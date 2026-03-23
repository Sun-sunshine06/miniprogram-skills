Page({
  data: {
    errorMessage: '',
    lastAction: 'idle',
    loading: false,
    title: 'Fixture Home',
  },

  handlePrimaryTap() {
    this.setData({
      lastAction: 'primary',
      title: 'Fixture Home',
    })
  },
})
