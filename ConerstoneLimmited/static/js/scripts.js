
function searchGoods() {
    const searchValue = document.getElementById('searchInput').value.toLowerCase();
    const filterBy = document.getElementById('filterBy').value;
    const table = document.getElementById('goodsTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
      const cells = rows[i].getElementsByTagName('td');
      let found = false;

      for (let j = 0; j < cells.length; j++) {
        const cellValue = cells[j].textContent.toLowerCase();

        if ((filterBy === 'all' || j === parseInt(filterBy)) && cellValue.includes(searchValue)) {
          found = true;
          break;
        }
      }

      if (found) {
        rows[i].style.display = '';
      } else {
        rows[i].style.display = 'none';
      }
    }
}
