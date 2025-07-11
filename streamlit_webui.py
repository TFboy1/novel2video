import streamlit as st
import requests
import json
from PIL import Image
import os
from io import BytesIO

# 配置API基础URL
API_BASE_URL = "http://localhost:1198/api"

# 设置页面配置
st.set_page_config(
    page_title="小说视觉化助手",
    page_icon="📚",
    layout="wide"
)

# 创建侧边栏导航
st.sidebar.title("导航")
page = st.sidebar.radio("选择功能", [
    "首页",
    "小说管理",
    "角色管理",
    "图像生成",
    "视频生成",
    "提示词管理",
    "模型配置"
])

# 首页
if page == "首页":
    st.title("📚 小说视觉化助手")
    st.write("""
    欢迎使用小说视觉化助手！这个工具可以帮助您：
    - 管理小说文本
    - 创建和管理角色
    - 根据小说内容生成图像
    - 将图像合成为视频
    - 管理提示词和模型配置

    请使用左侧的导航菜单选择您需要的功能。
    """)

    # 显示一些示例图片
    st.subheader("示例作品")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://picsum.photos/seed/novel1/300/200.jpg", caption="示例场景1")
    with col2:
        st.image("https://picsum.photos/seed/novel2/300/200.jpg", caption="示例场景2")
    with col3:
        st.image("https://picsum.photos/seed/novel3/300/200.jpg", caption="示例场景3")

# 小说管理
elif page == "小说管理":
    st.title("📖 小说管理")

    tab1, tab2, tab3 = st.tabs(["加载小说", "保存小说", "片段管理"])

    with tab1:
        st.subheader("加载小说")
        novel_url = st.text_input("输入小说URL或上传小说文件")
        if st.button("加载小说"):
            if novel_url:
                try:
                    response = requests.get(f"{API_BASE_URL}/novel/load")
                    if response.status_code == 200:
                        st.success("小说加载成功！")
                        st.text_area("小说内容预览", response.text[:1000], height=300)
                    else:
                        st.error(f"加载失败: {response.text}")
                except Exception as e:
                    st.error(f"请求失败: {str(e)}")
            else:
                st.warning("请输入小说URL")

        uploaded_file = st.file_uploader("或上传小说文件", type=["txt"])
        if uploaded_file is not None:
            try:
                files = {'file': uploaded_file}
                response = requests.post(f"{API_BASE_URL}/novel/save", files=files)
                if response.status_code == 200:
                    st.success("小说保存成功！")
                else:
                    st.error(f"保存失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab2:
        st.subheader("保存小说")
        novel_text = st.text_area("输入小说内容", height=300)
        if st.button("保存小说"):
            try:
                response = requests.post(f"{API_BASE_URL}/novel/save", json={"novel": novel_text})
                if response.status_code == 200:
                    st.success("小说保存成功！")
                else:
                    st.error(f"保存失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab3:
        st.subheader("片段管理")
        st.write("管理小说片段，用于生成图像和视频")

        if st.button("获取片段"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/fragments")
                if response.status_code == 200:
                    fragments = response.json()
                    st.success("片段获取成功！")

                    # 显示片段列表
                    for i, fragment in enumerate(fragments):
                        st.markdown(f"**片段 {i + 1}:**")
                        st.text_area(f"内容", fragment, height=100, key=f"fragment_{i}")
                else:
                    st.error(f"获取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

        if st.button("保存片段"):
            try:
                response = requests.post(f"{API_BASE_URL}/novel/fragments")
                if response.status_code == 200:
                    st.success("片段保存成功！")
                else:
                    st.error(f"保存失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

# 角色管理
elif page == "角色管理":
    st.title("🎭 角色管理")

    tab1, tab2, tab3 = st.tabs(["生成角色", "本地角色", "随机角色"])

    with tab1:
        st.subheader("生成新角色")
        num_characters = st.number_input("输入要生成的角色数量", min_value=1, max_value=10, value=1)
        if st.button("生成角色"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/characters?count={num_characters}")
                if response.status_code == 200:
                    characters = response.json()
                    st.success(f"成功生成 {len(characters)} 个角色！")

                    # 显示角色信息
                    for i, char in enumerate(characters):
                        with st.expander(f"角色 {i + 1}: {char.get('name', '未命名')}"):
                            st.json(char)
                else:
                    st.error(f"生成失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab2:
        st.subheader("本地角色")
        if st.button("获取本地角色"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/characters/local")
                if response.status_code == 200:
                    characters = response.json()
                    st.success(f"找到 {len(characters)} 个本地角色！")

                    # 显示角色列表
                    for i, char in enumerate(characters):
                        with st.expander(f"角色 {i + 1}: {char.get('name', '未命名')}"):
                            st.json(char)
                else:
                    st.error(f"获取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab3:
        st.subheader("随机角色")
        if st.button("生成随机角色"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/characters/random")
                if response.status_code == 200:
                    character = response.json()
                    st.success("成功生成随机角色！")

                    # 显示角色信息
                    st.json(character)
                else:
                    st.error(f"生成失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

# 图像生成
elif page == "图像生成":
    st.title("🖼️ 图像生成")

    tab1, tab2, tab3 = st.tabs(["一键生成", "重新生成", "本地图像"])

    with tab1:
        st.subheader("一键生成所有图像")
        if st.button("生成所有图像"):
            try:
                response = requests.post(f"{API_BASE_URL}/novel/images")
                if response.status_code == 200:
                    st.success("图像生成任务已提交！")
                    st.json(response.json())
                else:
                    st.error(f"生成失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab2:
        st.subheader("重新生成指定图像")
        image_id = st.text_input("输入要重新生成的图像ID")
        if st.button("重新生成"):
            try:
                response = requests.post(f"{API_BASE_URL}/novel/image", json={"id": image_id})
                if response.status_code == 200:
                    st.success("图像重新生成成功！")
                    st.image(response.json().get("image_url", ""), caption="新生成的图像")
                else:
                    st.error(f"生成失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab3:
        st.subheader("本地图像")
        if st.button("获取本地图像"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/images")
                if response.status_code == 200:
                    images = response.json()
                    st.success(f"找到 {len(images)} 张本地图像！")

                    # 显示图像列表
                    for i, img_info in enumerate(images):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(img_info.get("url", ""), width=150)
                        with col2:
                            st.json(img_info)
                else:
                    st.error(f"获取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

# 视频生成
elif page == "视频生成":
    st.title("🎬 视频生成")

    tab1, tab2 = st.tabs(["生成视频", "查看视频"])

    with tab1:
        st.subheader("生成视频")
        quality = st.selectbox("选择视频质量", ["low", "medium", "high"])
        fps = st.number_input("帧率", min_value=10, max_value=60, value=24)

        if st.button("生成视频"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/novel/video",
                    json={"quality": quality, "fps": fps}
                )
                if response.status_code == 200:
                    st.success("视频生成任务已提交！")
                    st.json(response.json())
                else:
                    st.error(f"生成失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab2:
        st.subheader("查看视频")
        if st.button("获取视频列表"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/video")
                if response.status_code == 200:
                    videos = response.json()
                    st.success(f"找到 {len(videos)} 个视频！")

                    # 显示视频列表
                    for i, video in enumerate(videos):
                        with st.expander(f"视频 {i + 1}: {video.get('name', '未命名')}"):
                            st.video(video.get("url", ""))
                            st.json(video)
                else:
                    st.error(f"获取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

# 提示词管理
elif page == "提示词管理":
    st.title("📝 提示词管理")

    tab1, tab2, tab3 = st.tabs(["场景提取", "英文提示词", "中文提示词"])

    with tab1:
        st.subheader("从文本提取场景")
        text = st.text_area("输入文本", height=200)
        if st.button("提取场景"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/novel/prompts",
                    json={"text": text}
                )
                if response.status_code == 200:
                    scenes = response.json()
                    st.success("场景提取成功！")
                    st.json(scenes)
                else:
                    st.error(f"提取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab2:
        st.subheader("英文提示词")
        prompt_en = st.text_area("输入英文提示词", height=100)
        if st.button("保存英文提示词"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/novel/prompt/en",
                    json={"prompt": prompt_en}
                )
                if response.status_code == 200:
                    st.success("英文提示词保存成功！")
                else:
                    st.error(f"保存失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

        if st.button("获取英文提示词"):
            try:
                response = requests.get(f"{API_BASE_URL}/novel/prompts/en")
                if response.status_code == 200:
                    prompt = response.json()
                    st.success("获取成功！")
                    st.text_area("英文提示词", prompt, height=100)
                else:
                    st.error(f"获取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab3:
        st.subheader("中文提示词")
        prompt_zh = st.text_area("输入中文提示词", height=100)
        if st.button("保存中文提示词"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/novel/prompt/zh",
                    json={"prompt": prompt_zh}
                )
                if response.status_code == 200:
                    st.success("中文提示词保存成功！")
                else:
                    st.error(f"保存失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

# 模型配置
elif page == "模型配置":
    st.title("⚙️ 模型配置")

    tab1, tab2 = st.tabs(["查看配置", "保存配置"])

    with tab1:
        st.subheader("当前模型配置")
        if st.button("获取配置"):
            try:
                response = requests.get(f"{API_BASE_URL}/model/config")
                if response.status_code == 200:
                    config = response.json()
                    st.success("获取配置成功！")
                    st.json(config)
                else:
                    st.error(f"获取失败: {response.text}")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

    with tab2:
        st.subheader("保存模型配置")
        config_json = st.text_area("输入JSON格式的配置", height=200)
        if st.button("保存配置"):
            try:
                config = json.loads(config_json)
                response = requests.post(
                    f"{API_BASE_URL}/model/config",
                    json=config
                )
                if response.status_code == 200:
                    st.success("配置保存成功！")
                else:
                    st.error(f"保存失败: {response.text}")
            except json.JSONDecodeError:
                st.error("JSON格式错误，请检查输入")
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

# 添加页脚
st.markdown("---")
st.markdown("📚 小说视觉化助手 &copy; 2025")
