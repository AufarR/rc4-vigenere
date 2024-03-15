import flet as ft
import shutil
from cipher import rc4

def main(page: ft.Page):
    page.title = "RC4 x Extended Vigenere Cipher"
    page.theme_mode = ft.ThemeMode.DARK
    
    page.fonts = {
        "Kalam": "/fonts/Kalam/Kalam-Regular.ttf",
        "JetBrainsMono": "/fonts/JetBrains_Mono/JetBrainsMono-VariableFont_wght.ttf",
        "SpaceGrotesk": "/fonts/Space_Grotesk/SpaceGrotesk-VariableFont_wght.ttf"
    }

    # func

    def download(file):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Text(value="Download"),
                    ft.Text(value=f"Download {file}"),
                    ft.ElevatedButton("Download", on_click=ft.FileResponse()),
                    ft.ElevatedButton("Back", on_click=lambda _: view_pop(page.views[-1])),
                ],
            )
        )
        page.update()
    


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def switchMode(value):
        page.mode = (
            "encrypt" if (page.mode=="decrypt") else "decrypt"

        )
        print(page.mode)
        c.label = (
            "Encrypt" if page.mode == "encrypt" else "Decrypt"
        )
        submit.text = page.mode.capitalize()
        inputtext.value = (
            "Plaintext" if page.mode == "encrypt" else "Ciphertext"
        )
        output.value = (
            "Ciphertext" if page.mode == "encrypt" else "Plaintext"
        )
        res.value = ""
        text_inputuser.value = ""

        page.update()
    
    def dialog_picker(e:ft.FilePickerResultEvent):
        print(e.files)
        for x in e.files:
            shutil.copy(x.path, f"uploads/{x.name}")
            selected_file.value = f"uploads/{x.name}"
            selected_file.update()


    def encrypt_decrypt(widget):
        # if file
        if selected_file.value != "":
            file = selected_file.value.split(", ")[0]
            with open(file, 'rb') as f:
                inputtext = memoryview(f.read())
            if page.mode == "encrypt":
                filename = file.split(".")[0]
                file_extension = file.split(".")[1]
                enc = rc4(inputtext, bytes(key_inputuser.value, 'utf-8'), True)
                with open(f"{filename}_encrypted.{file_extension}", "wb") as f:
                    f.write(enc)
                res.value = f"{filename}_encrypted.{file_extension}"
                # go to download
                
            else:
                filename = file.split(".")[0]
                file_extension = file.split(".")[1]
                dec = rc4(inputtext, bytes(key_inputuser.value, 'utf-8'), False)
                with open(f"{filename}_decrypted.{file_extension}", "wb") as f:
                    f.write(dec)
                res.value = f"{filename}_decrypted.{file_extension}"
                # go to download
            download(res.value)
            page.update()
            return

        if page.mode == "encrypt":
            plain = bytearray(text_inputuser.value, 'utf-8')
            enc = rc4(plain, bytes(key_inputuser.value, 'utf-8'))
            result = enc.hex().upper()
            # b64 = base64.b64encode(res.encode()).decode()
        else:
            cipher = bytes.fromhex(text_inputuser.value)
            dec = rc4(cipher, bytes(key_inputuser.value, 'utf-8'), False)
            result = dec.decode()

        res.value = result
        page.update()

    
    page.theme = ft.Theme(font_family="Jet")
    page.add(ft.Text(value="RC4 x Extended Vigenere Cipher"))
    page.mode = 'encrypt'

    c = ft.Switch(value=True, label='Encrypt', thumb_color={ft.MaterialState.SELECTED: ft.colors.BLUE}, active_color=ft.colors.BLUE,
        focus_color=ft.colors.BLUE, on_change=switchMode)
    page.add(c)
    inputtext = ft.Text(value="Plaintext")
    page.add(inputtext)
    text_inputuser = ft.TextField(value="")
    page.add(text_inputuser)

    selected_file = ft.Text("")

    


    Mypick = ft.FilePicker(on_result=dialog_picker)
    page.overlay.append(Mypick)


    page.add(
		ft.Column([
			ft.ElevatedButton("Insert file",
		on_click=lambda _: Mypick.pick_files()
			),
		selected_file

			])

		)

    page.add(ft.Text(value="Key"))

    key_inputuser = ft.TextField(value="")
    page.add(key_inputuser)
    submit = ft.FilledButton(text=page.mode.capitalize() ,on_click=encrypt_decrypt)
    page.add(submit)

    output = ft.Text(value="Ciphertext")
    page.add(output)
    res = ft.TextField(value="")
    page.add(res)

    

ft.app(target=main)

