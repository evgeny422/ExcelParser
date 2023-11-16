jQuery(document).ready(function () {
    $(document).on({
        'change': function (e) {
            const input = $(e.target);
            const targetName = input.data('filename-target');
            if (targetName) {
                const file = input.prop('files')[0];
                if (file) {
                    $(targetName).text(file.name);
                } else {
                    $(targetName).text("Файл не выбран");
                }
            }
        }
    }, '.input-file input')
});