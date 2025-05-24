// Get references
const messageBox = document.getElementById('messageBox');
const fontSelector = document.getElementById('fontSelector');
const styleSelector = document.getElementById('styleSelector');

// Function to update styles live in the message box
function updateMessageBoxStyles() {
  // Reset font classes
  messageBox.classList.remove('indie', 'marker', 'shadows', 'architects');
  // Reset style classes
  messageBox.classList.remove('bold', 'italic', 'underline');

  // Apply font class
  const fontValue = fontSelector.value;
  if (fontValue !== 'default') {
    messageBox.classList.add(fontValue);
  }

  // Apply style class
  const styleValue = styleSelector.value;
  if (styleValue !== 'default') {
    messageBox.classList.add(styleValue);
  }
}

// Listen for changes in both selectors
fontSelector.addEventListener('change', updateMessageBoxStyles);
styleSelector.addEventListener('change', updateMessageBoxStyles);
