import Mock from 'mockjs'
import itemApi from './item'

// 延时
Mock.setup({
  timeout: '200-2000'
})

// 项目相关
Mock.mock(/\/item\/getData/, 'get', itemApi.getItemData())
