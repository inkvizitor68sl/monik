;
(function($, document, window) {
  $(document).ready(function(){

    // setup checkbox if row clicked
    $('#events-tbl tr').click(function(event) {
      if (event.target.type !== 'checkbox') {
        $(':checkbox', this).trigger('click');
      }
    });

    // downtime button
    $('#set-downtime-btn').on('click', function() {
      // get all active checkboxes
      var activeCheckboxes = $('#events-tbl input[type=checkbox]:checked');
      if (!activeCheckboxes.length) {
        alert('Ни одной проверки не выбрано!');
        return ;
      }

      // get a downtime
      var downtime = prompt('Downtime в секундах', 0);
      if (downtime === null) {
        return ;
      }

      // for each checkbox send a downtime api
      activeCheckboxes.each(function(index, element) {
        var check = this;
        var hostname = $(check).data('hostname');
        var checkname = $(check).data('checkname');

        $.ajax({
          url: '/downtime',
          headers: {
            'Hostname': hostname,
            'Checkname': checkname,
            'Downtime-secs': +downtime
          },
          method: 'get',
          success: function() {
            $(check).prop('checked', false);
            $(check).parent().parent().removeClass();
          }
        });
      });
    });
  });
})(jQuery, document, window);
