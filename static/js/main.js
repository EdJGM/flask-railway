const btnDelte = document.querySelectorAll('.btn-delete');

if (btnDelte) {
    const btnArray = Array.from(btnDelte);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure?')) {
                e.preventDefault();
            }
        });
    });
}