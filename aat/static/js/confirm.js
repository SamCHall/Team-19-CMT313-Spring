function confirmDelete(link) {
    if (confirm("All detailed submission data for this assessment will be deleted. A simplified version will still remain. Are you sure you want to delete?")) {
      window.location.href = link.href;
      return true;
    } else {
      return false;
    }
  }

function confirmDeleteQ(link) {
  if (confirm("Are you sure you would like to delete this question?")) {
    window.location.href = link.href;
    return true;
  } else {
    return false;
  }
}
  