# IDMatcherPro GUI - Flet Version

import flet as ft
import re

def parse_entries(entries_content, entry_type):
    pattern = rf'<public type="{entry_type}" name="([a-zA-Z0-9_]+)" id="(0x[0-9a-fA-F]+)" />'
    return {name: id_value for name, id_value in re.findall(pattern, entries_content)}

def update_fields(fields_content, entries_dict):
    updated = []
    for line in fields_content.splitlines():
        match = re.match(r'\.field public static final ([a-zA-Z0-9_]+):I = (0x[0-9a-fA-F]+)', line.strip())
        if match:
            name = match.group(1)
            correct_id = entries_dict.get(name)
            if correct_id:
                updated.append(f".field public static final {name}:I = {correct_id}")
            else:
                updated.append(f"// Tidak ditemukan: {line}")
        else:
            updated.append(f"// Format tidak valid: {line}")
    return "\n".join(updated)

def main(page: ft.Page):
    page.title = "ID Matcher Pro - Flet Version"
    page.theme_mode = ft.ThemeMode.DARK
    page.fields_text = ""
    page.entries_text = ""

    entry_type = ft.TextField(label="Entry Type", width=300)
    result_output = ft.TextField(label="Result Output", multiline=True, expand=True, read_only=True)

    fields_filename = ft.Text(value="No fields file selected")
    entries_filename = ft.Text(value="No entries file selected")

    def pick_fields_result(e: ft.FilePickerResultEvent):
        if e.files:
            with open(e.files[0].path, 'r', encoding='utf-8') as f:
                page.fields_text = f.read()
            fields_filename.value = f"Selected: {e.files[0].name}"
            page.update()

    def pick_entries_result(e: ft.FilePickerResultEvent):
        if e.files:
            with open(e.files[0].path, 'r', encoding='utf-8') as f:
                page.entries_text = f.read()
            entries_filename.value = f"Selected: {e.files[0].name}"
            page.update()

    file_picker_fields = ft.FilePicker(on_result=pick_fields_result)
    file_picker_entries = ft.FilePicker(on_result=pick_entries_result)

    def run_match(e):
        et = entry_type.value.strip()
        entries_dict = parse_entries(page.entries_text, et)
        result = update_fields(page.fields_text, entries_dict)
        result_output.value = result
        page.update()

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    page.overlay.extend([file_picker_fields, file_picker_entries])

    page.add(
        ft.Row([
            ft.Column([
                ft.Text("ID Matcher Pro", size=28, weight=ft.FontWeight.BOLD),
                ft.Switch(label="Dark Mode", value=True, on_change=toggle_theme),
                entry_type,
                ft.ElevatedButton("Select Fields File", on_click=lambda _: file_picker_fields.pick_files()),
                fields_filename,
                ft.ElevatedButton("Select Entries File", on_click=lambda _: file_picker_entries.pick_files()),
                entries_filename,
                ft.ElevatedButton("Run Match", on_click=run_match),
                ft.Divider(),
                ft.Text("App by EasyWinter", italic=True, size=12, color=ft.Colors.GREY),
            ], spacing=10, width=400),
            ft.VerticalDivider(),
            ft.Column([
                result_output
            ], expand=True)
        ], expand=True)
    )

ft.app(target=main)
