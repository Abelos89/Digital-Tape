function Execute() {
    scriptText = document.getElementById("scriptTextArea").value;

    eval(scriptText);
}

function ClearScript() {
    document.getElementById("scriptTextArea").value = "";
}
