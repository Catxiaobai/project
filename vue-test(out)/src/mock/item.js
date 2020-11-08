import Mock from 'mockjs'

export default {
  getItemData: () => {
    return {
      code: 20000,
      data: {
        itemData: [
          {
            item_id: Mock.Random.increment(),
            item_name: Mock.Random.ctitle(2)
          },
          {
            item_id: Mock.Random.increment(),
            item_name: Mock.Random.ctitle(2)
          },
          {
            item_id: Mock.Random.increment(),
            item_name: Mock.Random.ctitle(2)
          }
          // {
          //   name: 'item_name',
          //   value: Mock.Random.ctitle(2)
          // }
        ]
      }
    }
  }
}
