<#
.SYNOPSIS
  Apunta el parametro RutaOrigen del modelo a la carpeta OrigenDatos de ESTA copia del proyecto.

.DESCRIPTION
  El repositorio se publica con un valor neutro (C:\RUTA_LOCAL\IADAY\OrigenDatos) para no exponer rutas
  personales. Ejecute este script una vez despues de clonar y ANTES de abrir IADAY.pbip en Power BI Desktop.
  Solo cambia el valor del parametro en IADAY.SemanticModel\definition\expressions.tmdl.

  Antes de hacer un commit, restaure el valor neutro con -Restaurar.

.EXAMPLE
  .\scripts\configurar_ruta.ps1              # configura la ruta de esta copia
  .\scripts\configurar_ruta.ps1 -Restaurar   # vuelve al valor neutro (antes de un commit)
#>
param([switch]$Restaurar)

$ErrorActionPreference = 'Stop'
$raiz = Split-Path $PSScriptRoot -Parent
$tmdl = Join-Path $raiz 'IADAY.SemanticModel\definition\expressions.tmdl'
$neutro = 'C:\RUTA_LOCAL\IADAY\OrigenDatos'
$destino = if ($Restaurar) { $neutro } else { Join-Path $raiz 'OrigenDatos' }

if (-not (Test-Path $tmdl)) { throw "No se encuentra $tmdl. Ejecute el script desde una copia completa del proyecto." }
if (-not $Restaurar -and -not (Test-Path $destino)) { throw "No se encuentra la carpeta $destino." }

$texto = [IO.File]::ReadAllText($tmdl)
$patron = '(expression RutaOrigen = ")[^"]*(")'
if (-not [regex]::IsMatch($texto, $patron)) { throw 'No se encontro el parametro RutaOrigen en expressions.tmdl.' }

$nuevo = [regex]::Replace($texto, $patron, [System.Text.RegularExpressions.MatchEvaluator] {
    param($m) $m.Groups[1].Value + $destino + $m.Groups[2].Value })
[IO.File]::WriteAllText($tmdl, $nuevo, (New-Object System.Text.UTF8Encoding($false)))

Write-Host "RutaOrigen = $destino"
if (-not $Restaurar) { Write-Host 'Listo. Abra IADAY.pbip en Power BI Desktop y haga clic en Actualizar.' }
