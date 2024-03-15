import flet as ft
from cipher import rc4
import base64
from time import time

async def main(page: ft.Page):

    # Function variables
    filePath = ""
    encrypt = True

    # Handlers

    async def handleCipher(e:ft.ControlEvent):
        nonlocal filePath, encrypt
        encrypt = False
        if e.control.text == "Encrypt":
            encrypt = True
        try:
            if inputFileBox.visible:
                with open(filePath, "rb") as f:
                    text = f.read()
            else:
                text = bytes(inputTextBox.value,'utf-8') if encrypt else base64.b64decode(inputTextBox.value)
            key = bytes(inputKeyBox.value,'utf-8')
            cipher_result = rc4(text,key,encrypt)
            outputBox.value = base64.b64encode(cipher_result).decode() if encrypt else cipher_result.decode()
            outputBox.update()
        except:
            outputBox.value = "ERROR" + (": Key must not be empty" if len(inputKeyBox.value) == 0 else "")
            outputBox.update()
    
    async def changeInput(e):
        inputFileBox.visible, inputTextBox.visible = inputTextBox.visible, inputFileBox.visible
        content.update()
    
    async def fileSelected(e:ft.FilePickerResultEvent):
        nonlocal filePath, encrypt
        inputFileInfo.value = e.files[0].name
        filePath = e.files[0].path
        inputFileInfo.update()
    
    async def fileSave(e:ft.FilePickerResultEvent):
        nonlocal encrypt
        fileName = "/{:s}_{:d}.txt".format('ciphertext' if encrypt else 'plaintext',int(time())) \
            if inputTextBox.visible else (f"/encrypted_{int(time())}.bin" if encrypt else f"/decrypted_{int(time())}.bin")
        with open(e.path+fileName,"wb") as f:
            f.write(base64.b64decode(outputBox.value) if encrypt else bytes(outputBox.value,'utf-8'))

    async def copyOutput(e):
        page.set_clipboard(outputBox.value)
    
    # Components
    
    inputFilePicker = ft.FilePicker(on_result=fileSelected)
    outputFilePicker = ft.FilePicker(on_result=fileSave)
    page.overlay.append(inputFilePicker)
    page.overlay.append(outputFilePicker)

    inputTextBox = ft.TextField(label="Input text", multiline=True,max_lines=8)
    inputKeyBox = ft.TextField(label="Key", password=True, can_reveal_password=True)
    inputFileButton = ft.FilledButton("Select a file", on_click=inputFilePicker.pick_files)
    inputFileInfo = ft.Text("No file selected")
    inputFileBox = ft.Row(
        [
            inputFileButton,
            inputFileInfo
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        visible=False
    )
    inputSwitch = ft.Row(
        [
            ft.Text("Upload file", size=18),
            ft.Switch(on_change=changeInput)
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    inputSubmitButtons = ft.Row(
        [
            ft.FilledButton(text="Encrypt", on_click=handleCipher),
            ft.FilledTonalButton(text="Decrypt", on_click=handleCipher)
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    outputBox = ft.TextField(label="Result (Base64)",multiline=True,read_only=True,max_lines=8)
    outputButtons = ft.Row(
        [
            ft.FilledButton(text="Save",on_click=outputFilePicker.get_directory_path),
            ft.FilledTonalButton(text="Copy",on_click=copyOutput)
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )

    # Main content

    content = ft.SafeArea (
        ft.Container (
            ft.Column(
                [
                    ft.Text("RC4 + Vigenere",size=36),
                    inputSwitch,
                    inputTextBox,
                    inputFileBox,
                    inputKeyBox,
                    inputSubmitButtons,
                    outputBox,
                    outputButtons,
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            )
        )
    )
    
    page.add(content)
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

ft.app(target=main)