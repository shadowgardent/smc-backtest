param (
    [string]$docxPath,
    [string]$pdfPath
)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    # 17 is wdExportFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0)
    Write-Output "Successfully converted $docxPath to $pdfPath"
} catch {
    Write-Error $_
} finally {
    $word.Quit()
}
