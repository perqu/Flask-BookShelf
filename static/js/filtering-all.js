function filteringAll() {
  let start_date = document.getElementById("start").value;
  let end_date = document.getElementById("end").value;
  let keyword = document.getElementById("search").value;
  let table = document.getElementById("table");
  let all_tr = table.getElementsByTagName("tr");

  keyword = keyword.toUpperCase();

  for (let i = 0; i < all_tr.length; i++) {
    let title_column = all_tr[i].getElementsByTagName("td")[1];
    let authors_column = all_tr[i].getElementsByTagName("td")[2];
    let published_column = all_tr[i].getElementsByTagName("td")[3];
    let language_column = all_tr[i].getElementsByTagName("td")[8];

    console.log(language_column);

    if (title_column && authors_column && published_column && language_column) {
      let title_value = title_column.textContent || title_column.innerText;
      let authors_value = authors_column.textContent;
      let published_value = published_column.textContent;
      let language_value = language_column.textContent;

      title_value = title_value.toUpperCase();
      authors_value = authors_value.toUpperCase();
      language_value = language_value.toUpperCase();

      if (
        title_value.indexOf(keyword) > -1 ||
        authors_value.indexOf(keyword) > -1 ||
        language_value.indexOf(keyword) > -1
      ) {
        if (published_value >= start_date && published_value <= end_date) {
          all_tr[i].style.display = ""; // show
        } else if (published_value >= start_date && !end_date) {
          all_tr[i].style.display = ""; // show
        } else if (published_value <= end_date && !start_date) {
          all_tr[i].style.display = ""; // show
        } else if (!end_date && !start_date) {
          all_tr[i].style.display = ""; // show
        } else {
          all_tr[i].style.display = "none";
        }
      } else {
        all_tr[i].style.display = "none"; // hide
      }
    }
  }
}
