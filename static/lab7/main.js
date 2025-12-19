// Функция для заполнения таблицы фильмов
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function(data) {
            return data.json();
        })
        .then(function(films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            for(let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');
                tdActions.className = 'actions-cell';
                
                // Оригинальное название курсивом, если оно отличается от русского
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<span class="original-title">${films[i].title}</span>`;
                } else {
                    tdTitle.innerHTML = '<span class="original-title">—</span>';
                }
                
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;
                
                let editButton = document.createElement('button');
                editButton.className = 'edit-btn';
                editButton.innerText = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(i);
                };
                
                let delButton = document.createElement('button');
                delButton.className = 'delete-btn';
                delButton.innerText = 'Удалить';
                delButton.onclick = function() {
                    deleteFilm(i, films[i].title_ru);
                };
                
                tdActions.append(editButton);
                tdActions.append(delButton);
                
                tr.append(tdTitle);
                tr.append(tdTitleRus);
                tr.append(tdYear);
                tr.append(tdActions);
                
                tbody.append(tr);
            }
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильмов:', error);
            alert('Не удалось загрузить список фильмов. Пожалуйста, обновите страницу.');
        });
}

// Функция для удаления фильма
function deleteFilm(id, title) {
    if(!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function(response) {
            if (response.status === 204) {
                fillFilmList();
            } else {
                alert('Не удалось удалить фильм');
            }
        })
        .catch(function(error) {
            console.error('Ошибка при удалении фильма:', error);
            alert('Произошла ошибка при удалении фильма');
        });
}

// Функция для редактирования фильма
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(data) {
            return data.json();
        })
        .then(function(film) {
            document.getElementById('modal-title').innerText = 'Редактировать фильм';
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            
            // Очистка ошибок
            document.getElementById('description_error').innerText = '';
            document.getElementById('title_ru_error').innerText = '';
            document.getElementById('title_error').innerText = '';
            document.getElementById('year_error').innerText = '';
            
            showModal();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке данных фильма:', error);
            alert('Не удалось загрузить данные фильма для редактирования');
        });
}

// Функция для показа модального окна
function showModal() {
    document.getElementById('film-modal').style.display = 'block';
}

// Функция для скрытия модального окна
function hideModal() {
    document.getElementById('film-modal').style.display = 'none';
}

// Функция для отмены (закрытия модального окна)
function cancel() {
    hideModal();
}

// Функция для добавления нового фильма
function addFilm() {
    document.getElementById('modal-title').innerText = 'Добавить фильм';
    document.getElementById('id').value = "";
    document.getElementById('title').value = "";
    document.getElementById('title_ru').value = "";
    document.getElementById('year').value = "";
    document.getElementById('description').value = "";
    
    // Очистка ошибок
    document.getElementById('description_error').innerText = '';
    document.getElementById('title_ru_error').innerText = '';
    document.getElementById('title_error').innerText = '';
    document.getElementById('year_error').innerText = '';
    
    showModal();
}

// Функция для отправки данных фильма (добавление или редактирование)
function sendFilm() {
    const id = document.getElementById('id').value;
    const title = document.getElementById('title').value;
    const title_ru = document.getElementById('title_ru').value;
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value;
    
    // Базовые проверки на фронтенде
    if (!title_ru.trim()) {
        document.getElementById('title_ru_error').innerText = 'Русское название обязательно';
        return;
    }
    
    if (!year) {
        document.getElementById('year_error').innerText = 'Год обязателен';
        return;
    }
    
    if (!description.trim()) {
        document.getElementById('description_error').innerText = 'Описание обязательно';
        return;
    }
    
    const film = {
        title: title,
        title_ru: title_ru,
        year: parseInt(year),
        description: description
    };
    
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
    // Очистка предыдущих ошибок
    document.getElementById('description_error').innerText = '';
    document.getElementById('title_ru_error').innerText = '';
    document.getElementById('title_error').innerText = '';
    document.getElementById('year_error').innerText = '';
    
    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            return resp.json();
        } else {
            return resp.json().then(function(errors) {
                throw errors;
            });
        }
    })
    .then(function(data) {
        fillFilmList();
        hideModal();
    })
    .catch(function(errors) {
        // Отображение ошибок валидации
        if (errors.description) {
            document.getElementById('description_error').innerText = errors.description;
        }
        if (errors.title_ru) {
            document.getElementById('title_ru_error').innerText = errors.title_ru;
        }
        if (errors.title) {
            document.getElementById('title_error').innerText = errors.title;
        }
        if (errors.year) {
            document.getElementById('year_error').innerText = errors.year;
        }
        
        // Если это не ошибки валидации, а другая ошибка
        if (errors.error && !errors.description && !errors.title_ru && !errors.title && !errors.year) {
            alert(`Ошибка: ${errors.error}`);
        }
    });
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('film-modal');
    if (event.target == modal) {
        hideModal();
    }
}

// Вызов функции заполнения таблицы при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});