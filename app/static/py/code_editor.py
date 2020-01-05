from browser import document, window

editor = window.ace.edit("editor")
editor.setTheme("ace/theme/monokai")
textarea = document.select('#code')[0]


def on_code_change(*args):
    textarea.value = editor.getSession().getValue()


editor.getSession().on("change", on_code_change)
on_code_change()

editor.setOptions({
    'enableBasicAutocompletion': True,
    'enableLiveAutocompletion': True,
    'showLineNumbers': True,
    'tabSize': 4
})
editor.session.setMode("ace/mode/python")
