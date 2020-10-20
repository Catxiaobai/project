<template>
  <div id="common-header" class="common-header">
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
      <div id="mainMenu">
        <el-menu id="el-menu" default-active="2" mode="horizontal" @select="handleSelect" text-color="#fff" active-text-color="#ffd04b">
          <div id="headMenu">
            <el-menu-item index="2">平台信息管理</el-menu-item>
            <el-menu-item index="3">安全性数据库管理</el-menu-item>
          </div>
          <div id="itemMenu" class="itemMenu" v-show="divSubMenuVisible">
            <span style="text-align: center;margin-top: 15px;font-family: 华文行楷;font-size: 24px;width: 100px">
              {{ itemInfo.item_name }}
            </span>
            <el-menu-item index="0">软件安全性分析</el-menu-item>
            <el-menu-item index="1">软件安全性设计</el-menu-item>
            <el-button icon="el-icon-close" circle @click="closeSubMenu"></el-button>
          </div>
          <!--        <el-menu-item index="4">项目管理</el-menu-item>-->
        </el-menu>
      </div>
      <!--      <div id="subMenu" v-show="divSubMenuVisible">-->
      <!--        <div id="itemTitle" class="itemTitle">-->
      <!--          <span>{{ itemInfo.item_name }}</span>-->
      <!--          <el-button icon="el-icon-close" circle @click="closeSubMenu"></el-button>-->
      <!--        </div>-->
      <!--        <div id="itemMenu" class="itemMenu">-->
      <!--          <el-button @click="selectAnalysis">软件安全性分析</el-button>-->
      <!--          <el-button @click="selectDesign">软件安全性设计</el-button>-->
      <!--          &lt;!&ndash;            <el-menu-item index="0">软件安全性分析</el-menu-item>&ndash;&gt;-->
      <!--          &lt;!&ndash;            <el-menu-item index="1">软件安全性设计</el-menu-item>&ndash;&gt;-->
      <!--        </div>-->
      <!--      </div>-->
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
      activeIndex: '2',
      divSubMenuVisible: false,
      itemInfo: {
        item_content: '',
        item_date: null,
        item_id: 0,
        item_introduction: '',
        item_name: ''
      },
      headMenu: [],
      menuList: [
        [
          {
            path: '/safetyAnalysis/modeling',
            name: 'modeling',
            label: '使用场景建模',
            icon: 's-claim',
            children: [
              // {
              //   path: '/subScene',
              //   name: 'subScene',
              //   label: '子使用场景建模',
              //   children: [
              //     {
              //       path: '/subSceneInfo',
              //       name: 'subSceneInfo',
              //       label: '子使用场景描述'
              //     },
              //     {
              //       path: '/subSceneModel',
              //       name: 'subSceneModel',
              //       label: '子使用场景建模'
              //     }
              //   ]
              // },
              {
                path: '/subSceneInfo',
                name: 'subSceneInfo',
                label: '子使用场景描述'
              },
              {
                path: '/subSceneModel',
                name: 'subSceneModel',
                label: '子使用场景建模'
              },
              // {
              //   path: '/complexScene',
              //   name: 'complexScene',
              //   label: '综合场景建模',
              //   children: [
              //     {
              //       path: '/complexSceneInfo',
              //       name: 'complexSceneInfo',
              //       label: '综合使用场景描述'
              //     },
              //     {
              //       path: '/complexSceneModel',
              //       name: 'complexSceneModel',
              //       label: '综合使用场景建模'
              //     }
              //   ]
              // },
              {
                path: '/complexSceneInfo',
                name: 'complexSceneInfo',
                label: '综合使用场景描述'
              },
              {
                path: '/complexSceneModel',
                name: 'complexSceneModel',
                label: '综合使用场景建模'
              },
              {
                path: '/listGeneration',
                name: 'listGeneration',
                label: '模型列表生成'
              }
            ]
          },
          {
            path: '/safetyAnalysis/analysisRules',
            name: 'analysisRules',
            label: '分析规则设置',
            icon: 's-claim',
            children: [
              {
                path: '/specialRules',
                name: 'specialRules',
                label: '项目分析规则设置'
              },
              {
                path: '/generalRules',
                name: 'generalRules',
                label: '通用分析规则选择'
              }
            ]
          },
          {
            path: '/safetyAnalysis/implement',
            name: 'implement',
            label: '分析实施',
            icon: 's-claim',
            children: [
              {
                path: '/check',
                name: 'check',
                label: '模型检验'
              },
              {
                path: '/failureAnalysis',
                name: 'failureAnalysis',
                label: '失效分析'
              },
              {
                path: '/demandExtraction',
                name: 'demandExtraction',
                label: '软件安全性需求提取'
              }
            ]
          },
          {
            path: '/safetyAnalysis/requirements',
            name: 'requirements',
            label: '软件安全性需求管理',
            icon: 's-claim'
          }
        ],
        [
          {
            path: '/safetyDesign/criteria',
            name: 'criteria',
            label: '设计准则设置',
            icon: 's-claim',
            children: [
              {
                path: '/generalCriteria',
                name: 'generalCriteria',
                label: '通用设计准则选择'
              },
              {
                path: '/specialCriteria',
                name: 'specialCriteria',
                label: '专用设计准则设置'
              }
            ]
          },
          {
            path: '/safetyDesign/verification',
            name: 'verification',
            label: '核查实施',
            icon: 's-claim'
          },
          {
            path: '/safetyDesign/complete',
            name: 'complete',
            label: '设计完善',
            icon: 's-claim'
          }
        ],
        [
          {
            path: '/infoManage/system',
            name: 'system',
            label: '系统管理',
            icon: 's-claim',
            children: [
              {
                path: '/personnel',
                name: 'personnel',
                label: '人员管理'
              },
              {
                path: '/authority',
                name: 'authority',
                label: '权限管理'
              },
              {
                path: '/tools',
                name: 'tools',
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
            path: '/database/analysisBase',
            name: 'analysisBase',
            label: '分析规则库',
            icon: 's-claim'
          },
          {
            path: '/database/designBase',
            name: 'designBase',
            label: '设计准则库',
            icon: 's-claim'
          }
        ]
      ]
    }
  },
  mounted() {
    this.getItemInfo()
    this.activeIndex = this.$route.path
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
      console.log(this.menuList[key])
      this.bus.$emit('transferMenuData', this.menuList[key])
    },
    selectAnalysis() {
      this.bus.$emit('transferMenuData', this.menuList[0])
    },
    selectDesign() {
      this.bus.$emit('transferMenuData', this.menuList[1])
    },
    closeSubMenu() {
      this.divSubMenuVisible = false
      this.bus.$emit('transferMenuData', this.menuList[2])
    },
    gotoHome() {
      this.$router.replace('/main')
    },
    gotoLogin() {
      // window.location.href = '/'
      this.$router.replace('/login')
    },
    getItemInfo() {
      this.bus.$on('itemInfo', msg => {
        this.itemInfo = msg
        console.log(this.itemInfo)
        this.divSubMenuVisible = true
      })

      // this.divSubMenuVisible = true
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
    //width: 100%;
    background: #545c64;
    display: flex;
    #mainMenu {
      height: 100%;
      //width: 60%;
      #el-menu {
        display: flex;
        height: 100%;
        width: 100%;
      }
    }
    //#subMenu {
    //  width: 400px;
    //  height: 100%;
    //  //background: greenyellow;
    //  #itemTitle {
    //    height: 40%;
    //    margin-top: 5.5px;
    //    margin-left: 45%;
    //    //text-align: center;
    //    background: greenyellow;
    //  }
    //  #itemMenu {
    //    height: 50%;
    //    margin-top: 0;
    //    background: yellow;
    //  }
    //}
  }
}

#itemMenu {
  //background: white;
  //background: #545c64;
  display: flex;
  //height: 80%;
}
#headMenu {
  //background: gold;
  background: #545c64;
  display: flex;
}
</style>
<style lang="scss">
.itemMenu {
  .el-menu-item {
    height: 95%;
    //margin-top: 10px;
    background: #545c64;
    //display: flex;
  }
  .el-button {
    width: 20px;
    height: 20px;
    padding: 0;
    margin-top: 15px;
    margin-left: 15px;
    margin-right: 15px;
  }
}
.itemTitle {
  .el-button {
    //height: 10px;
    //border: 0;
    padding: 0;
    margin: 0 0 0 60%;
  }
}
</style>
