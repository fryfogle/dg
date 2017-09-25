export const navsConfig = {
  'navs': {
    'Home': {
      'active': true,
      'filters': true,
      'import': {
        'overall': false,
        'recent': false,
      },
      'classes': {
        'container1': 'col-md-11',
      },
      'addTab': true,
      'containers': {
        'container1': {
          'Trainings Conducted': {
            'addDivs': ['state_trainer_#trainings','state_trainer_#mediators','question_wise_data','year_month_wise_data']
          },
        }
      }
    }
  }
}
