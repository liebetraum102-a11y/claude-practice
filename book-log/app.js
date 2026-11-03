// localStorage에 저장할 때 쓰는 이름
const STORAGE_KEY = "books";

// 저장된 데이터가 없을 때 처음 한 번만 넣는 책들
const INITIAL_BOOKS = [
  { id: 1, title: "어린왕자", author: "생텍쥐페리", rating: 5, review: "" },
  { id: 2, title: "아몬드", author: "손원평", rating: null, review: "" },
  { id: 3, title: "달의 지배자", author: "N.K. 제미신", rating: null, review: "" },
];

// 저장된 책 목록을 읽어 온다. 처음 열었다면 초기 데이터를 먼저 저장한다.
function loadBooks() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved === null) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_BOOKS));
    return INITIAL_BOOKS;
  }
  return JSON.parse(saved);
}

// 책 목록을 화면에 그린다.
function renderBooks(books) {
  const list = document.getElementById("book-list");
  list.innerHTML = "";

  for (const book of books) {
    const rating = book.rating === null ? "평점 없음" : "★".repeat(book.rating);
    const item = document.createElement("li");
    item.textContent = `${book.title} - ${book.author} (${rating})`;
    if (book.review !== "") {
      item.textContent += ` : ${book.review}`;
    }
    list.appendChild(item);
  }
}

renderBooks(loadBooks());
