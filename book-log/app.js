// localStorage에 저장할 때 쓰는 이름
const STORAGE_KEY = "books";

// 날짜 기능이 생기기 전에 넣은 책들의 입력 날짜 (2026년 11월 9일)
const LEGACY_ADDED_AT = new Date(2026, 10, 9).toISOString(); // 월은 0부터 시작해서 10 = 11월

// 저장된 데이터가 없을 때 처음 한 번만 넣는 책들
const INITIAL_BOOKS = [
  { id: 1, title: "어린왕자", author: "생텍쥐페리", rating: 5, review: "", addedAt: LEGACY_ADDED_AT, tags: [] },
  { id: 2, title: "아몬드", author: "손원평", rating: null, review: "", addedAt: LEGACY_ADDED_AT, tags: [] },
  { id: 3, title: "달의 지배자", author: "N.K. 제미신", rating: null, review: "", addedAt: LEGACY_ADDED_AT, tags: [] },
];

// "인생책, 소설 ,인생책" 같은 입력을 ["인생책", "소설"]로 정리한다. (공백·빈 값·중복 제거)
function parseTags(text) {
  const tags = text.split(",").map((tag) => tag.trim()).filter((tag) => tag !== "");
  return [...new Set(tags)];
}

// 저장된 책 목록을 읽어 온다. 처음 열었다면 초기 데이터를 먼저 저장한다.
function loadBooks() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved === null) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_BOOKS));
    return INITIAL_BOOKS;
  }

  // 예전에 저장된 책에 없는 항목을 채워서 다시 저장한다.
  // 날짜가 없으면 LEGACY_ADDED_AT, 태그가 없으면 빈 목록.
  const books = JSON.parse(saved);
  let changed = false;
  for (const book of books) {
    if (!book.addedAt) {
      book.addedAt = LEGACY_ADDED_AT;
      changed = true;
    }
    if (!Array.isArray(book.tags)) {
      book.tags = [];
      changed = true;
    }
  }
  if (changed) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
  }
  return books;
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
    if (book.tags.length > 0) {
      item.textContent += ` ${book.tags.map((tag) => `#${tag}`).join(" ")}`;
    }

    const tagButton = document.createElement("button");
    tagButton.type = "button";
    tagButton.textContent = "태그 수정";
    tagButton.addEventListener("click", () => editTags(book.id));
    item.append(" ", tagButton);

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "삭제";
    deleteButton.addEventListener("click", () => deleteBook(book.id));
    item.append(" ", deleteButton);

    list.appendChild(item);
  }
}

// 입력창으로 태그를 새로 받아 저장하고 목록을 다시 그린다.
function editTags(id) {
  const book = books.find((item) => item.id === id);
  const input = prompt(
    `"${book.title}"의 태그를 쉼표로 구분해 입력하세요. (모두 지우려면 비워 두세요)`,
    book.tags.join(", ")
  );
  if (input === null) {
    return; // 취소를 누르면 그대로 둔다.
  }

  book.tags = parseTags(input);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
  renderBooks(books);
}

// 확인을 받은 뒤 책을 지우고 목록을 다시 그린다.
function deleteBook(id) {
  const index = books.findIndex((book) => book.id === id);
  if (!confirm(`"${books[index].title}"을(를) 정말 삭제할까요?`)) {
    return;
  }

  books.splice(index, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
  renderBooks(books);
}

// ===== 데이터 내보내기 / 가져오기 =====

// 지금 목록을 books.json 형식(보기 좋게 줄바꿈)의 파일로 내려받는다.
function exportBooks() {
  const json = JSON.stringify(books, null, 2) + "\n";
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "books.json";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

// 파일에서 읽은 책 하나를 앱 형식에 맞게 정리한다. 제목·작가가 없으면 오류를 낸다.
function normalizeBook(raw, index) {
  const position = `${index + 1}번째 책`;
  if (typeof raw !== "object" || raw === null) {
    throw new Error(`${position}의 형식이 올바르지 않아요.`);
  }
  const title = typeof raw.title === "string" ? raw.title.trim() : "";
  const author = typeof raw.author === "string" ? raw.author.trim() : "";
  if (title === "" || author === "") {
    throw new Error(`${position}에 제목이나 작가가 없어요.`);
  }

  const rating = Number.isInteger(raw.rating) && raw.rating >= 1 && raw.rating <= 5 ? raw.rating : null;
  const addedAt =
    typeof raw.addedAt === "string" && !Number.isNaN(new Date(raw.addedAt).getTime())
      ? raw.addedAt
      : LEGACY_ADDED_AT;
  const tags = Array.isArray(raw.tags)
    ? parseTags(raw.tags.filter((tag) => typeof tag === "string").join(","))
    : [];

  return {
    id: raw.id,
    title,
    author,
    rating,
    review: typeof raw.review === "string" ? raw.review.trim() : "",
    addedAt,
    tags,
  };
}

// 파일 내용을 검사해서 책 목록으로 만든다. id가 없거나 겹치면 새 번호를 붙인다.
function parseBooksFile(text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error("JSON 파일 형식이 아니에요.");
  }
  if (!Array.isArray(data)) {
    throw new Error("책 목록([ ... ]) 형식이 아니에요.");
  }

  const imported = data.map(normalizeBook);
  const usedIds = new Set();
  let nextId = Math.max(0, ...imported.map((book) => (Number.isInteger(book.id) ? book.id : 0))) + 1;
  for (const book of imported) {
    if (!Number.isInteger(book.id) || book.id < 1 || usedIds.has(book.id)) {
      book.id = nextId++;
    }
    usedIds.add(book.id);
  }
  return imported;
}

// 고른 파일을 읽어서, 확인을 받은 뒤 지금 목록을 파일 내용으로 바꾼다.
async function importBooks(file) {
  let imported;
  try {
    imported = parseBooksFile(await file.text());
  } catch (error) {
    alert(`가져오지 못했어요: ${error.message}\n지금 목록은 그대로 두었어요.`);
    return;
  }

  const message =
    `"${file.name}"에서 책 ${imported.length}권을 찾았어요.\n` +
    `지금 목록(${books.length}권)을 이 내용으로 바꿀까요?\n` +
    `(지금 목록이 필요하면 먼저 [데이터 내보내기]로 백업해 두세요)`;
  if (!confirm(message)) {
    return;
  }

  books.splice(0, books.length, ...imported); // 같은 배열을 유지한 채 내용만 바꾼다.
  localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
  renderBooks(books);
  alert(`책 ${imported.length}권을 불러왔어요.`);
}

const books = loadBooks();
renderBooks(books);

document.getElementById("export-button").addEventListener("click", exportBooks);

const importFile = document.getElementById("import-file");
document.getElementById("import-button").addEventListener("click", () => importFile.click());
importFile.addEventListener("change", async () => {
  const file = importFile.files[0];
  if (file) {
    await importBooks(file);
  }
  importFile.value = ""; // 같은 파일을 다시 골라도 동작하게 비운다.
});

// 폼을 제출하면 새 책을 저장하고 목록을 다시 그린다.
const form = document.getElementById("book-form");
form.addEventListener("submit", (event) => {
  event.preventDefault(); // 페이지가 새로고침되지 않게 막는다.

  const title = document.getElementById("title").value.trim();
  const author = document.getElementById("author").value.trim();
  const rating = document.getElementById("rating").value;
  const review = document.getElementById("review").value.trim();
  const tags = parseTags(document.getElementById("tags").value);

  // 공백만 입력한 경우는 브라우저가 걸러 주지 않아서 직접 확인한다.
  if (title === "" || author === "") {
    alert("제목과 작가를 입력해 주세요.");
    return;
  }

  books.push({
    id: Math.max(0, ...books.map((book) => book.id)) + 1,
    title,
    author,
    rating: rating === "" ? null : Number(rating),
    review,
    addedAt: new Date().toISOString(), // 입력한 시각 (리포트에서 날짜 표시·정렬에 사용)
    tags,
  });
  localStorage.setItem(STORAGE_KEY, JSON.stringify(books));

  renderBooks(books);
  form.reset();
});
