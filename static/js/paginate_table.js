jQuery(document).ready(function () {
    console.log('23');
    $tables = new DataTable('table[data-table-type^=paginate-table-]', {
        dom: 'lt<"d-flex justify-content-center mt-2"p>',
        ordering: false,
        pageLength: 10,
        sLengthMenu: 'Количество элементов',
        lengthMenu: [[10, 20, 30, 40, -1], [10, 20, 30, 40, 'Все']],
        language: {
            oPaginate: {
                sNext: '<div class="d-flex align-content-center justify-content-center"><span class="svg-arrow i-left"></span></div>',
                sPrevious: '<div class="d-flex align-content-center justify-content-center"><span class="svg-arrow i-right"></span></div>',
            },
            lengthMenu: "Количество элементов _MENU_"
        }
    });
    console.log($tables);
});