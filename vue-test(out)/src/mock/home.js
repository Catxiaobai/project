import Mock from 'mockjs'

export default {
  getHomeData: () => {
    return {
      code: 20000,
      data: {
        itemData: [
          {
            name: 'item_id',
            value: Mock.Random.increment()
          },
          {
            name: 'item_name',
            value: Mock.Random.ctitle(2)
          }
        ]
      }
    }
  }
}
