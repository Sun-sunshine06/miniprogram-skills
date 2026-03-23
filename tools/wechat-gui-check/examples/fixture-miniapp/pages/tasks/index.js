Page({
  data: {
    activeScope: 'all',
    errorMessage: '',
    loading: false,
    scopes: ['all', 'week', 'done'],
    title: 'Fixture Tasks',
  },

  handleScopeTap(event) {
    const scope = event && event.currentTarget && event.currentTarget.dataset
      ? event.currentTarget.dataset.scope
      : 'all'

    this.setData({
      activeScope: scope || 'all',
    })
  },
})
