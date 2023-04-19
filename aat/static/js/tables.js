$.fn.dataTable.ext.type.order['difficulty-pre'] = function ( d ) {
   switch ( d ) {
  case '<span class="badge bg-very-easy">Very Easy></span>': return 1;
  case '<span class="badge bg-easy">Easy</span>': return 2;
  case '<span class="badge bg-medium">Medium</span>': return 3;
  case '<span class="badge bg-hard">Hard</span>': return 4;
  case '<span class="badge bg-very-hard">Very Hard</span>': return 5;
  case '': return 6;
  }
  return 0; };


$(document).ready(function() {
  $('button[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
});
 // fixes column widths on tab change

  $('#data-staff').DataTable( {
    "columnDefs": [
      { type: 'difficulty', "targets": 1 }
    ],
      "aoColumns": [
          { "bSortable": true },  // 0
          { "bSortable": true },  // 1
          { "bSortable": true },  // 2
          { "bSortable": false,
            "bSearchable": false }  // 3
      ]
  } );

  $('#data-staff-archive').DataTable( {
    "columnDefs": [
      { type: 'difficulty', "targets": 1 }
    ],
      "aoColumns": [
          { "bSortable": true },  // 0
          { "bSortable": true },  // 1
          { "bSortable": true },  // 2
          { "bSortable": false,
            "bSearchable": false }  // 3
      ]
  } );

  $('#data').DataTable( {
    "columnDefs": [
      { type: 'difficulty', "targets": 1 }
    ],
      "aoColumns": [
          { "bSortable": true }, // 0
          { "bSortable": true }, // 1
          { "bSortable": true }, // 2
          { "bSortable": true } // 3
      ]
  } );

  $('#data-student-list').DataTable( {
    "aoColumns": [
      { "bSortable" : true},
      { "bSortable" : true},
      {
        "bSortable" : false,
        "bSearchable": false
      }
    ]
  });

  $('#data-student-marks').DataTable( {
    "aoColumns": [
      { "bSortable" : true},
      { "bSortable" : true},
      { "bSortable" : true},
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      }
    ]
  });

  $('#data-student-module-overview').DataTable( {
    "aoColumns": [
      { "bSortable" : true},
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      }
    ]
  });

  $('.data-student-module-assessments').DataTable({
    "aoColumns": [
      { "bSortable" : true},
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      },
      {
        "bSortable" : true,
        "bSearchable": false
      }
    ]
  });
} );
