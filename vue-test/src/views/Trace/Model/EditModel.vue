<template>
  <div id="sample">
    <div class="divHelp">
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <p>此页面可以对使用场景进行动态编辑</p>
        <p>对模型每次操作都会触发验证，提示操作是否可行</p>
        <br />
        <p>新增空白节点：在空白处双击鼠标左键</p>
        <p>新增边：选定一个节点，将鼠标移至节点边缘处，长按鼠标左键，从该节点处延伸至另一节点处即可</p>
        <p>删除节点：鼠标左键单击进行选定，然后点击键盘上的"delete"或"Backspace"键</p>
        <p>删除边：鼠标左键单击进行选定，然后点击键盘上的"delete"或"Backspace"键</p>
        <p>移动节点：鼠标左键单击进行选定，将鼠标移至节点中心处，长按鼠标左键即可拖拽移动</p>
        <br />
        <p>模型还原：将模型还原至未修改前的初始状态</p>
        <el-button icon="el-icon-message-solid" circle slot="reference"></el-button>
      </el-popover>
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <div>
          <p>此页面可以对使用场景进行动态编辑</p>
          <p>对模型每次操作都会触发验证，提示操作是否可行</p>
          <br />
          <p>新增空白节点：在空白处双击鼠标左键</p>
          <p>新增边：选定一个节点，将鼠标移至节点边缘处，长按鼠标左键，从该节点处延伸至另一节点处即可</p>
          <p>删除节点：鼠标左键单击进行选定，然后点击键盘上的"delete"或"Backspace"键</p>
          <p>删除边：鼠标左键单击进行选定，然后点击键盘上的"delete"或"Backspace"键</p>
          <p>移动节点：鼠标左键单击进行选定，将鼠标移至节点中心处，长按鼠标左键即可拖拽移动</p>
        </div>
        <el-button type="text" slot="reference">操作提示</el-button>
      </el-popover>
    </div>
    <el-card>
      <!--      <el-button type="primary" @click="save">save</el-button>-->
      <!--      <el-button type="primary" @click="load">load</el-button>-->
      <span style="font-size: x-large;margin-left: 40%">模型动态编辑</span>
      <el-button type="primary" style="margin-left: 38%" @click="reduction">模型还原</el-button>
      <div id="myDiagramDiv" style="background-color: whitesmoke; border: solid 1px black; width: 100%; height: 520px;margin-top: 20px"></div>
      <textarea id="myTransaction" style="width:100%;height:200px" v-show="false"></textarea>
      <textarea id="mytest" v-model="msg" v-show="false" />
      <!--      <input id="mytest" value="test" @change="postData('test')" />-->
      <!--      <div id="example">-->
      <!--&lt;!&ndash;        <p>Original message: "{{ msg }}"</p>&ndash;&gt;-->
      <!--        &lt;!&ndash;        <p>Computed reversed message: "{{ reversedMessage }}"</p>&ndash;&gt;-->
      <!--      </div>-->
    </el-card>
  </div>
</template>

<script>
import go from 'gojs'
const MAKE = go.GraphObject.make
export default {
  name: 'PageThree.vue',
  data() {
    return {
      nodeDataArray: [],
      linkDataArray: [],
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: []
      },
      msg: 'result',
      test: 'tets'
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    save() {
      // document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      console.log(this.myDiagram.model.toJson())
      this.postData(this.myDiagram.model.toJson())
      this.text_data = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
    },
    load() {
      var model = go.Model.fromJson(this.text_data)

      model.makeUniqueKeyFunction = function(model, data) {
        var i = model.nodeDataArray.length * 2 + 1
        while (model.findNodeDataForKey(i) !== null) i += 2
        data.id = i // assume Model.nodeKeyProperty === "id"
        return i
      }
      // link data id's are even numbers
      model.makeUniqueLinkKeyFunction = function(model, data) {
        var i = model.linkDataArray.length * 2 + 2
        while (model.findLinkDataForKey(i) !== null) i += 2
        data.id = i // assume GraphLinksModel.linkKeyProperty === "id"
        return i
      }
      this.myDiagram.model = model
    },
    getData() {
      this.$http
        .get('http://127.0.0.1:8000/api/deliver_model')
        .then(response => {
          console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // console.log(this.text_data)
          this.load()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    // postData(data) {
    //   this.$http
    //     .post('http://127.0.0.1:8000/api/verify_action', { add: data })
    //     .then(response => {
    //       console.log(response.data)
    //       if (response.data.error_code === 0) {
    //         this.$message({
    //           type: 'success',
    //           message: response.data.result
    //         })
    //       }
    //     })
    //     .catch(function(error) {
    //       console.log(error)
    //     })
    // },
    init() {
      var element = document.getElementById('mytest')
      var $ = go.GraphObject.make
      this.myDiagram = $(go.Diagram, 'myDiagramDiv', {
        // have mouse wheel events zoom in and out instead of scroll up and down
        'toolManager.mouseWheelBehavior': go.ToolManager.WheelZoom,
        // support double-click in background creating a new node
        'clickCreatingTool.archetypeNodeData': { text: 'new node' },
        // InitialLayoutCompleted: function(e) {

        // enable undo & redo
        'undoManager.isEnabled': false,
        layout: $(go.ForceDirectedLayout, {
          defaultSpringLength: 40,
          defaultElectricalCharge: 180,
          randomNumberGenerator: null,
          infinityDistance: 210
        })
      })

      this.myDiagram.nodeTemplate = $(
        go.Node,
        'Auto',
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'name'))) // end of Adornment
        },
        new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
        // define the node's outer shape, which will surround the TextBlock

        // 图标的style
        $(go.Shape, 'Circle', {
          desiredSize: new go.Size(67, 67),
          fill: $(go.Brush, 'Linear', { 0: 'rgb(0,191,255)', 1: 'rgb(30,144,255)' }),
          stroke: 'black',
          portId: '',
          fromLinkable: true,
          fromLinkableSelfNode: true,
          fromLinkableDuplicates: true,
          toLinkable: true,
          toLinkableSelfNode: true,
          toLinkableDuplicates: true,
          cursor: 'pointer'
        }),
        // 字体的style
        $(
          go.TextBlock,
          {
            font: 'bold 11pt helvetica, bold arial, sans-serif',
            editable: true // editing the text automatically updates the model data
          },
          new go.Binding('text', 'text').makeTwoWay()
        )
      )
      this.myDiagram.linkTemplate = $(
        go.Link, // the whole link panel
        {
          curve: go.Link.Bezier,
          adjusting: go.Link.Stretch,
          reshapable: true,
          relinkableFrom: true,
          relinkableTo: true
        },
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $(
            'ToolTip',
            { 'Border.fill': 'whitesmoke', 'Border.stroke': 'black' },
            $(go.TextBlock, { margin: 4 }, new go.Binding('text', '', tooltipTextConverter))
          )
        },
        {
          click: function(e, obj) {
            console.log('e:' + e + '---obj:' + obj.part.data)
            console.log('Clicked on ' + obj.part.data.key)
          }
        },
        new go.Binding('points').makeTwoWay(),
        new go.Binding('curviness', 'curviness'),
        $(
          go.Shape, // the link shape
          { strokeWidth: 1.5 }
        ),
        $(
          go.Shape, // the arrowhead
          { toArrow: 'standard', stroke: null }
        ),
        $(
          go.Panel,
          'Auto',
          $(
            go.Shape, // the label background, which becomes transparent around the edges
            {
              fill: $(go.Brush, 'Radial', { 0: 'rgb(240, 240, 240)', 0.3: 'rgb(240, 240, 240)', 1: 'rgba(240, 240, 240, 0)' }),
              stroke: null
            }
          ),
          $(
            go.TextBlock,
            'transition', // the label text
            {
              textAlign: 'center',
              font: '10pt helvetica, arial, sans-serif',
              stroke: 'black',
              margin: 4,
              editable: true // editing the text automatically updates the model data
            },
            new go.Binding('text', 'text').makeTwoWay()
          )
        )
      )
      // unlike the normal selection Adornment, this one includes a Button
      this.myDiagram.nodeTemplate.selectionAdornmentTemplate = $(
        go.Adornment,
        'Spot',
        $(
          go.Panel,
          'Auto',
          $(go.Shape, { fill: null, stroke: 'blue', strokeWidth: 2 }),
          $(go.Placeholder) // this represents the selected Node
        )
        // the button to create a "next" node, at the top-right corner
        // $(
        //   'Button',
        //   {
        //     alignment: go.Spot.TopRight,
        //     click: addNodeAndLink // this function is defined below
        //   },
        //   $(go.Shape, 'PlusLine', { desiredSize: new go.Size(6, 6) })
        // ) // end button
      ) // end Adornment
      // and adds a link to that new node
      function addNodeAndLink(e, obj) {
        var adorn = obj.part
        e.handled = true
        var diagram = adorn.diagram
        diagram.startTransaction('Add State')

        // get the node data for which the user clicked the button
        var fromNode = adorn.adornedPart
        var fromData = fromNode.data
        // create a new "State" data object, positioned off to the right of the adorned Node
        var toData = { text: 'new' }
        var p = fromNode.location.copy()
        p.x += 100
        toData.loc = go.Point.stringify(p) // the "loc" property is a string, not a Point object
        // add the new node data to the model
        var model = diagram.model
        model.addNodeData(toData)

        // create a link data from the old node data to the new node data
        var linkdata = {
          from: model.getKeyForNodeData(fromData), // or just: fromData.id
          to: model.getKeyForNodeData(toData),
          text: 'transition'
        }
        // and add the link data to the model
        model.addLinkData(linkdata)

        // select the new Node
        var newnode = diagram.findNodeForData(toData)
        diagram.select(newnode)

        diagram.commitTransaction('Add State')

        // if the new node is off-screen, scroll the diagram to show the new node
        diagram.scrollToRect(newnode.actualBounds)
      }

      // this.myDiagram.addDiagramListener('addNodeAndLink', function() {
      //   console.log('test')
      // })
      // replace the default Link template in the linkTemplateMap

      function tooltipTextConverter(person) {
        var str = ''
        // console.log(person)
        // str += 'id: ' + person.id + '\n'
        str += 'name: ' + person.text + '\n'
        str += 'source: ' + person.from + '\n'
        str += 'target: ' + person.to + '\n'
        str += 'event: ' + person.event + '\n'
        str += 'condition: ' + person.cond + '\n'
        str += 'action: ' + person.action + '\n'
        return str
      }
      this.myDiagram.toolManager.hoverDelay = 10

      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('LinkRelinked', function(e) {
        console.log('线重连')
        // var data = { test: 'testjson' }
        // postDelData(data)
      })
      //添加监听文本编辑事件
      this.myDiagram.addDiagramListener('TextEdited', function(e) {
        console.log('文本编辑' + e)
      })
      // 监听删除事件
      this.myDiagram.addDiagramListener('SelectionDeleted', function(e) {
        console.log('删除')
        e.subject.each(function(n) {
          console.log('delete:' + JSON.stringify(n.data))
          //
          console.log('total:' + e.diagram.model.toJson())
          // 传递删除信息和剩下的信息
          var data = { total: e.diagram.model.toJson(), delete: JSON.stringify(n.data) }
          postDelData(data)
        })
      })
      // 监听添加线事件
      this.myDiagram.addDiagramListener('LinkDrawn', function(e) {
        console.log('add:' + JSON.stringify(e.subject.data))
        console.log('total:' + e.diagram.model.toJson())
        // 传递添加的信息和剩下的信息
        var data = { total: e.diagram.model.toJson(), add: JSON.stringify(e.subject.data) }
        postAddData(data)
      })
      // 向后端传递添加信息
      function postAddData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', 'http://127.0.0.1:8000/api/verify_add', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function() {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
            myFunction(json['result'])
          }
        }
      }
      // todo 删除一个节点会进行多次判断
      // 向后端传递添删除信息
      function postDelData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', 'http://127.0.0.1:8000/api/verify_del', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function() {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
            myFunction(json['result'])
          }
        }
      }
      function myFunction(res) {
        var x
        var r = confirm(res)
        if (r == true) {
          x = '你按下了"确定"按钮!'
        } else {
          x = '你按下了"取消"按钮!'
        }
        // document.getElementById('demo').innerHTML = x
      }
    },
    reduction() {
      console.log('模型还原')
    }
  },
  created() {
    this.getData()
  }
}
</script>

<style lang="scss" scoped>
.divHelp {
  margin-left: 1100px;
  height: 40px;
  margin-top: -40px;
}
</style>
