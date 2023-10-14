// Simple tab functionality
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tabs li a');
  const tabContents = document.querySelectorAll('.tabs div');

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', (event) => {
      event.preventDefault();
      hideAllTabs();
      tabContents[index].style.display = 'block';
    });
  });

  // Helper function to hide all tab contents
  function hideAllTabs() {
    tabContents.forEach((content) => {
      content.style.display = 'none';
    });
  }
});
