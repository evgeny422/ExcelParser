jQuery(document).ready(function () {
    $tables = new DataTable('table[data-table-type^=paginate-table-]', {
        dom: 't<"d-flex justify-content-center mt-2"p>',
        ordering: false,
        pageLength: 5,
        language: {
            oPaginate: {
                sNext: '<div class="d-flex align-content-center justify-content-center"><span class="svg-arrow i-left"></span></div>',
                sPrevious: '<div class="d-flex align-content-center justify-content-center"><span class="svg-arrow i-right"></span></div>',
            }
        }
    });
    console.log($tables);
});