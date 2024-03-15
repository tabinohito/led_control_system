import flet as ft
import flet.canvas as cv
import random
import time
from paho.mqtt import client as mqtt_client
from mqtt_connect import MqttConnect

# コンポーネントの作成
class LED_Controller(ft.UserControl):
    def __init__(self):
        super().__init__()
        #描画線の初期設定
        self.line = ft.Paint( 
            stroke_width = 3,
            color = "black",
            style = "stroke",
            stroke_cap = "round"
        )

        self.area_name = ["STAND_AREA_0", "STAND_AREA_1", "STAND_AREA_2", "STAND_AREA_3", "STAND_AREA_4", "STAND_AREA_5", "STAND_AREA_6", "STAND_AREA_7"]
        self.area_status = ["RED_ON", "RED_BLINK", "BOTH_OFF", "BLUE_BLINK", "BLUE_ON"]
        self.host = '172.17.0.1'
        self.port = 1883
        self.client_id = f'publish-{random.randint(0, 1000)}'

        self.mqtt = MqttConnect(self.client_id, self.host, self.port)
        self.mqtt_send_time = 0

        self.segment = []
    
    # テキストボタンをクリックしたときの処理
    def button_clicked(self, e):
        for x,i in enumerate(self.area_name):
            self.segment[x].selected_icon.name=ft.icons.FLASHLIGHT_OFF
            # red area
            selected = self.segment[x].selected.pop()
            if "RED" in selected:
                print(selected)
                self.segment[x].selected_icon.color=ft.colors.RED
                self.segment[x].selected_icon.name=ft.icons.FLASHLIGHT_OFF
            # blue area
            elif "BLUE" in selected:
                self.segment[x].selected_icon.color=ft.colors.BLUE
                self.segment[x].selected_icon.name=ft.icons.FLASHLIGHT_OFF
            else:
                self.segment[x].selected_icon.color=ft.colors.BLACK
                self.segment[x].selected_icon.name=ft.icons.FLASHLIGHT_OFF

            self.segment[x].selected = False
            # self.segment[x].selected.add(i + "_BOTH_OFF")

            # self.mqtt.publish(i, "BOTH_OFF")
            # time.sleep(0.25)
        self.update()
        return e

    # スライダーが変更されたときの処理
    def slider_change(self, e):
        self.line = ft.Paint(
            # 線の太さにスライダーの値を代入
            # stroke_width = int(e.control.value),
            color = "black",
            style = "stroke",
            stroke_cap = "round"
        )

        print((e.control.value / 100) * 255)
        if time.time() - self.mqtt_send_time > 0.2:
            self.mqtt.publish("LED_BRIGHTNESS", str(int((e.control.value / 100) * 255)))
            self.mqtt_send_time = time.time()

    # SegmentedButtonが変更されたときの処理
    def segment_change(self,e):
        segment_name = e.control.selected.pop()

        area_name = ""
        for i in self.area_name:
            if i in segment_name:
                area_name = i
                break

        status = ""
        for i in self.area_status:
            if i in segment_name:
                status = i
                break

        self.mqtt.publish(area_name, status)

        # if status == "BOTH_OFF":
        #     print(e.control.selected_icon)
        return e
    
    # クラスの返り値の設定
    def build(self):
        # テキストボタンの作成
        self.button = ft.TextButton(
            text = "CLEAR LEDs",  # 表示するテキスト
            on_click = self.button_clicked  # クリックしたときの処理
        )
        
        # Slider & Text
        self.text = ft.Text(
            "LED Brightness: 0-255",
            size=50,  # サイズ(default:14)
            expand = True,
            weight=ft.FontWeight.W_900,  # 太さ(default:NORMAL
        )
        self.slider = ft.Slider(
            min = 0,  # 最小値
            max = 100,  # 最大値
            divisions = 10,  # 最小値から最大値の間の分割数
            value = 50,  # 初期値
            label = "{value}%",  # スライダーを変更したときに表示されるテキスト
            expand = True,
            on_change = self.slider_change, #スライダーが変更されたときの処理
        )
            
        # SegmentedButton
        for i in range(len(self.area_name)):
            self.segment.append(
                ft.SegmentedButton(
                        selected_icon=ft.Icon(
                        name=ft.icons.FLASHLIGHT_ON,
                        color=ft.colors.YELLOW
                    ),
                    selected={self.area_name[i] +"_BOTH_OFF"},
                    on_change = self.segment_change,
                    style=ft.ButtonStyle(
                        ft.colors.WHITE,
                        ft.colors.GREEN,
                        ft.colors.BLACK,
                    ),
                    segments=[
                        ft.Segment(
                            value= self.area_name[i] + "_RED_ON",
                            label=ft.Text("RED OCCUPIED"),
                            icon=ft.Icon(
                                name=ft.icons.FLASHLIGHT_OFF,
                                color=ft.colors.RED
                            ),

                        ),
                        ft.Segment(
                            value= self.area_name[i] + "_RED_BLINK",
                            label=ft.Text("RED INSTRUCTION"),
                            icon=ft.Icon(
                                name=ft.icons.FLASHLIGHT_OFF,
                                color=ft.colors.RED
                            ),
                        ),
                        ft.Segment(
                            value= self.area_name[i] + "_BOTH_OFF",
                            label=ft.Text("NULL"),
                            icon=ft.Icon(
                                name=ft.icons.FLASHLIGHT_OFF,
                                color=ft.colors.BLACK
                            ),
                        ),
                        ft.Segment(
                            value= self.area_name[i] + "_BLUE_BLINK",
                            label=ft.Text("BLUE INSTRUCTION"),
                            icon=ft.Icon(
                                name=ft.icons.FLASHLIGHT_OFF,
                                color=ft.colors.BLUE
                            ),
                        ),
                        ft.Segment(
                            value= self.area_name[i] + "_BLUE_ON",
                            label=ft.Text("BLUE OCCUPIED"),
                            icon=ft.Icon(
                                name=ft.icons.FLASHLIGHT_OFF,
                                color=ft.colors.BLUE
                            ),
                        ),
                    ],
                )
            )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.button,
                        *self.segment,
                        self.text,
                        self.slider,
                    ], spacing=20
                ), padding=20
            ), margin=20
        )

        # return ft.Column(
        #     [
        #         self.button,
        #         *self.segment,
        #         self.text,
        #         self.slider,
        #     ]
        # )

def main(page: ft.Page):
    page.title = "LED Controller"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    view = LED_Controller()  # インスタンス化
    # ページに追加
    page.add(
        ft.Container(
            content = view,
            expand = True  # コントロールの大きさをウィンドウに合わせる
            )
        )
    

if __name__ == "__main__":
    ft.app(target=main)