function confirmDelete(link) {
    if (confirm("Are you sure you want to delete?")) {
      window.location.href = link.href;
      return true;
    } else {
      return false;
    }
  }
  