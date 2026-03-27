Page({
  data: {
    actionPayloadSource: 'idle',
    errorMessage: '',
    lastAction: 'idle',
    loading: false,
    title: 'Fixture Home',
  },

  handlePrimaryTap() {
    this.setData({
      actionPayloadSource: 'tap',
      lastAction: 'primary',
      title: 'Fixture Home',
    })
  },

  applyScenario(payload) {
    const nextPayload = payload && typeof payload === 'object' ? payload : {}

    this.setData({
      actionPayloadSource: nextPayload.payloadSource || 'callMethod',
      lastAction: nextPayload.lastAction || 'method',
      title: nextPayload.title || 'Fixture Home',
    })
  },
})
