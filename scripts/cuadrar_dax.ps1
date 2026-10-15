<#
.SYNOPSIS
  Cuadra las medidas DAX del modelo IADAY contra los KPIs recalculados por validar_kpis.py.

.DESCRIPTION
  1. Ejecuta `python scripts/validar_kpis.py --json` para obtener los valores esperados.
  2. Consulta cada medida en una instancia local de Analysis Services (Power BI Desktop con el modelo
     cargado y refrescado) mediante ADOMD.
  3. Compara y escribe docs/cuadre-dax.md. Código de salida 1 si algo no cuadra.

.PARAMETER Puerto
  Puerto de la instancia local de Analysis Services (archivo msmdsrv.port.txt del workspace de Desktop).

.PARAMETER Base
  Nombre de la base de datos (catálogo) del modelo cargado.

.EXAMPLE
  .\scripts\cuadrar_dax.ps1 -Puerto 62481 -Base IADAY_test
#>
param(
    [Parameter(Mandatory = $true)][int]$Puerto,
    [Parameter(Mandatory = $true)][string]$Base
)
$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
$json = Join-Path ([IO.Path]::GetTempPath()) 'iaday_esperado.json'

python (Join-Path $raiz 'scripts\validar_kpis.py') --json $json | Out-Null
$esp = [IO.File]::ReadAllText($json, [Text.Encoding]::UTF8) | ConvertFrom-Json

$dll = Get-ChildItem 'C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Microsoft.AnalysisServices.AdomdClient' -Recurse -Filter *.dll | Select-Object -First 1
Add-Type -Path $dll.FullName
$cn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$Puerto;Initial Catalog=$Base")
$cn.Open()

function Consultar([string]$dax) {
    $cmd = $cn.CreateCommand(); $cmd.CommandText = $dax
    $rd = $cmd.ExecuteReader(); $filas = @()
    while ($rd.Read()) {
        $f = [ordered]@{}
        for ($i = 0; $i -lt $rd.FieldCount; $i++) { $f[$rd.GetName($i)] = $rd.GetValue($i) }
        $filas += [pscustomobject]$f
    }
    $rd.Close(); $filas
}

$res = New-Object System.Collections.Generic.List[object]
function Comparar([string]$ambito, [string]$medida, $esperado, $obtenido) {
    if ($esperado -is [string]) { $ok = ($esperado -eq [string]$obtenido) }
    else { $ok = ([math]::Abs([double]$esperado - [double]$obtenido) -le 1e-6 * [math]::Max(1, [math]::Abs([double]$esperado))) }
    $res.Add([pscustomobject]@{ Ambito = $ambito; Medida = $medida; Esperado = $esperado; DAX = $obtenido; OK = $ok })
}

# --- globales
$medidas = $esp.global.PSObject.Properties.Name
$args2 = ($medidas | ForEach-Object { '"' + $_ + '", [' + $_ + ']' }) -join ', '
$fila = (Consultar "EVALUATE ROW($args2)")[0]
foreach ($m in $medidas) { Comparar 'Global' $m $esp.global.$m $fila."[$m]" }

# --- por iniciativa
$dax = 'EVALUATE SUMMARIZECOLUMNS(dim_proyecto[id_proyecto], "t", [Total Actividades], "c", [Completadas], "b", [Bloqueadas], "v", [Vencidas], "d", [Desvío Global], "s", [Semáforo Iniciativa])'
foreach ($r in (Consultar $dax)) {
    $id = $r.'dim_proyecto[id_proyecto]'
    $e = $esp.por_iniciativa.$id
    Comparar $id 'Total Actividades' $e.'Total Actividades' $r.'[t]'
    Comparar $id 'Completadas' $e.Completadas $r.'[c]'
    Comparar $id 'Bloqueadas' $e.Bloqueadas $r.'[b]'
    Comparar $id 'Vencidas' $e.Vencidas $r.'[v]'
    Comparar $id 'Desvío Global' $e.'Desvío Global' $r.'[d]'
    Comparar $id 'Semáforo Iniciativa' $e.'Semáforo Iniciativa' $r.'[s]'
}
$cn.Close()

# --- reporte
$fallos = @($res | Where-Object { -not $_.OK })
$L = New-Object System.Collections.Generic.List[string]
$L.Add('# Cuadre de medidas DAX contra el validador')
$L.Add('')
$L.Add("> Generado por ``scripts/cuadrar_dax.ps1``. Fecha de corte: **$([datetime]::Parse($esp.corte).ToString('dd/MM/yyyy'))**. Esperado = ``scripts/validar_kpis.py``; DAX = medidas del modelo ``IADAY.SemanticModel``.")
$L.Add('')
$L.Add("**Resultado: $(if ($fallos.Count -eq 0) { 'CUADRA' } else { 'NO CUADRA' })** — $($res.Count - $fallos.Count)/$($res.Count) comparaciones correctas.")
$L.Add('')
$L.Add('| Ámbito | Medida | Esperado (validador) | Obtenido (DAX) | OK |')
$L.Add('|---|---|---|---|---|')
$ci = [Globalization.CultureInfo]::InvariantCulture
foreach ($r in $res) {
    $e = if ($r.Esperado -is [string]) { $r.Esperado } else { ([double]$r.Esperado).ToString('0.######', $ci) }
    $d = if ($r.DAX -is [string]) { $r.DAX } else { ([double]$r.DAX).ToString('0.######', $ci) }
    $L.Add("| $($r.Ambito) | $($r.Medida) | $e | $d | $(if ($r.OK) { '✅' } else { '❌' }) |")
}
[IO.File]::WriteAllText((Join-Path $raiz 'docs\cuadre-dax.md'), ($L -join "`n") + "`n", (New-Object Text.UTF8Encoding($false)))
Write-Output "Comparaciones: $($res.Count - $fallos.Count)/$($res.Count) correctas"
$fallos | Format-Table -AutoSize | Out-String | Write-Output
if ($fallos.Count -gt 0) { exit 1 }
