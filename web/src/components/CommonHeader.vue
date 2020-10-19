<template>
  <div id="common-header">
    <div id="top">
      <div id="left-content">
        <div id="imgLogo">
          <el-image :src="imgLogo"></el-image>
        </div>
        <div id="leftTitle">
          <span>{{ title }}</span>
        </div>
      </div>
      <div id="right-content">
        <div id="rightTitle">
          <el-link @click="gotoHome">首页</el-link> |
          <el-link @click="gotoLogin">退出</el-link>
        </div>
      </div>
    </div>
    <div id="bottom">
      <el-menu id="headMenu" mode="horizontal" @select="handleSelect" text-color="#fff" active-text-color="#ffd04b">
        <el-menu-item index="0">软件安全性分析</el-menu-item>
        <el-menu-item index="1">软件安全性设计</el-menu-item>
        <el-menu-item index="2">平台信息管理</el-menu-item>
        <el-menu-item index="3">安全性数据库管理</el-menu-item>
        <!--        <el-menu-item index="4">项目管理</el-menu-item>-->
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommonHeader.vue',
  data() {
    return {
      title: '基于使用场景的软件安全性分析与设计工具',
      imgLogo: require('@/assets/images/logo.png'),
      activeIndex: '1',
      headMenu: [],
      menuList: [
        [
          {
            path: '/one',
            name: 'one',
            label: '使用场景建模',
            icon: 's-claim',
            children: [
              {
                path: '/login',
                name: 'login',
                label: '子使用场景建模'
              },
              {
                path: '/login',
                name: 'login',
                label: '综合场景建模'
              },
              {
                path: '/login',
                name: 'login',
                label: '模型列表生成'
              }
            ]
          },
          {
            path: '/two',
            name: 'two',
            label: '分析规则设置',
            icon: 's-claim',
            children: [
              {
                path: '/login',
                name: 'login',
                label: '项目分析规则设置'
              },
              {
                path: '/login',
                name: 'login',
                label: '通用分析规则选择'
              }
            ]
          },
          {
            path: '/three',
            name: 'three',
            label: '分析实施',
            icon: 's-claim',
            children: [
              {
                path: '/login',
                name: 'login',
                label: '模型检验'
              },
              {
                path: '/login',
                name: 'login',
                label: '失效分析'
              },
              {
                path: '/login',
                name: 'login',
                label: '软件安全性需求提取'
              }
            ]
          },
          {
            path: '/four',
            name: 'four',
            label: '软件安全性需求管理',
            icon: 's-claim'
          }
        ],
        [
          {
            path: '/three',
            name: 'three',
            label: '设计准则设置',
            icon: 's-claim',
            children: [
              {
                path: '/login',
                name: 'login',
                label: '通用设计准则选择'
              },
              {
                path: '/login',
                name: 'login',
                label: '专用设计准则设置'
              }
            ]
          },
          {
            path: '/four',
            name: 'four',
            label: '核查实施',
            icon: 's-claim'
          },
          {
            path: '/four',
            name: 'four',
            label: '设计完善',
            icon: 's-claim'
          }
        ],
        [
          {
            path: '/five',
            name: 'five',
            label: '系统管理',
            icon: 's-claim',
            children: [
              {
                path: '/login',
                name: 'login',
                label: '人员管理'
              },
              {
                path: '/login',
                name: 'login',
                label: '权限管理'
              },
              {
                path: '/login',
                name: 'login',
                label: '工具说明'
              }
            ]
          },
          {
            path: '/infoManage/item',
            name: 'item',
            label: '项目管理',
            icon: 's-claim'
          }
        ],
        [
          {
            path: '/six',
            name: 'six',
            label: '分析规则库',
            icon: 's-claim'
          },
          {
            path: '/six',
            name: 'six',
            label: '设计规则库',
            icon: 's-claim'
          }
        ]
      ]
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
      console.log(this.menuList[key])
      this.bus.$emit('transferMenuData', this.menuList[key])
    },
    gotoHome() {
      this.$router.replace('/home')
    },
    gotoLogin() {
      // window.location.href = '/'
      this.$router.replace('/login')
    }
  }
}
</script>

<style scoped lang="scss">
#common-header {
  background: #f5f9f9;
  width: 100%;
  height: 96px;
  display: flex;
  flex-direction: column;
  #top {
    display: flex;
    height: 60px;
    #left-content {
      width: 100%;
      display: flex;
      #imgLogo {
        //height: 60px;
        width: 65px;
      }
      #leftTitle {
        height: 60px;
        font-size: xx-large;
        font-weight: bold;
        font-family: 楷体;
        margin-top: 10px;
        margin-left: 20px;
      }
    }
    #right-content {
      width: 100px;
      float: right;
      #rightTitle {
        margin-top: 20px;
      }
    }
  }
  #bottom {
    height: 100%;
    background: skyblue;
    #headMenu {
      background-color: #545c64;
    }
  }
}
</style>
