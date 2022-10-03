function copy() {
    let copyText = document.getElementById("shortenurl");


    copyText.select();

    // for mobile
    copyText.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(copyText.value);

    inform = document.getElementById('balloon');
    if (inform.style.display == "none") {
        inform.style.display = "table";
    }
}