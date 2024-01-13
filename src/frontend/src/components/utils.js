// Enable Tabs in the editor.
export function do_tab(e) {
	if (e.keyCode === 9) { // tab was pressed
		e.preventDefault();
    // get caret position/selection
    var val = e.target.value,
        start = e.target.selectionStart,
        end = e.target.selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    e.target.value = val.substring(0, start) + '\t' + val.substring(end);

    // put caret at right position again
    e.target.selectionStart = e.target.selectionEnd = start + 1;

    // prevent the focus lose
    return false;
  }
}

export function close_window() {
  window.open('','_parent','');
  window.close();
}
