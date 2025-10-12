# pylint: disable=invalid-name
import os
import uuid

import streamlit as st
from langchain_core.messages import HumanMessage

from agents.agent import Agent
from agents.receptionist_agent import ReceptionistAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent


def initialize_agents():
    if 'agent' not in st.session_state:
        st.session_state.agent = Agent()
    if 'receptionist_agent' not in st.session_state:
        st.session_state.receptionist_agent = ReceptionistAgent()
    if 'knowledge_base_agent' not in st.session_state:
        st.session_state.knowledge_base_agent = KnowledgeBaseAgent()


def render_travel_assistant():
    st.title("AI差旅助手")
    st.write("欢迎使用AI差旅助手。请用自然语言提出您的差旅需求，并提供相关的差旅政策和个人偏好。")

    with st.expander("差旅政策与偏好"):
        budget = st.number_input("预算（元）", min_value=0, value=5000)
        hotel_standard = st.selectbox("酒店标准", ["三星级", "四星级", "五星级"], index=1)

    user_input = st.text_area(
        '差旅需求',
        height=150,
        key='travel_query',
        placeholder='例如：“下周我要去北京出差三天，帮我预订机票和酒店”',
    )

    if st.button('提交'):
        if user_input:
            full_query = f"""
            请根据以下信息规划行程：
            需求: {user_input}
            政策和偏好:
            - 预算上限: {budget}元
            - 酒店标准: {hotel_standard}
            """
            try:
                thread_id = str(uuid.uuid4())
                st.session_state.thread_id = thread_id

                messages = [HumanMessage(content=full_query)]
                config = {'configurable': {'thread_id': thread_id}}

                with st.spinner('正在为您规划行程...'):
                    result = st.session_state.agent.graph.invoke({'messages': messages}, config=config)

                st.session_state.travel_info = result['messages'][-1].content

            except Exception as e:
                st.error(f'Error: {e}')
        else:
            st.error('请输入您的差旅需求。')

    if 'travel_info' in st.session_state:
        st.subheader('差旅信息')
        st.markdown(st.session_state.travel_info)

        st.subheader("自动报销")
        if st.button("生成报销申请"):
            reimbursement_prompt = f"""
            请根据以下差旅信息，并遵循标准公司报销政策，生成一份详细的报销申请单。
            报销申请应包括项目、日期、金额和总计。

            差旅信息:
            {st.session_state.travel_info}
            """
            try:
                messages = [HumanMessage(content=reimbursement_prompt)]
                config = {'configurable': {'thread_id': st.session_state.thread_id}}

                with st.spinner('正在生成报销申请...'):
                    reimbursement_result = st.session_state.agent.graph.invoke({'messages': messages}, config=config)

                st.subheader("报销申请草稿")
                st.markdown(reimbursement_result['messages'][-1].content)

            except Exception as e:
                st.error(f'Error generating reimbursement: {e}')


def render_receptionist():
    st.title("AI接待")
    st.write("欢迎使用AI接待。请选择您需要的功能。")

    receptionist_options = ["访客管理", "会议室预订"]
    selection = st.radio("请选择功能", receptionist_options)

    if selection == "访客管理":
        st.subheader("访客管理")
        visitor_name = st.text_input("访客姓名")
        employee_name = st.text_input("被访员工姓名")
        if st.button("登记"):
            notification_prompt = f"为{employee_name}生成一条通知，告知他们访客{visitor_name}已经到达。"
            try:
                messages = [HumanMessage(content=notification_prompt)]

                with st.spinner('正在生成通知...'):
                    notification_result = st.session_state.receptionist_agent.graph.invoke({'messages': messages})

                st.success(notification_result['messages'][-1].content)

            except Exception as e:
                st.error(f'Error generating notification: {e}')

    elif selection == "会议室预订":
        st.subheader("会议室预订")
        attendees = st.number_input("与会人数", min_value=1, value=1)
        duration = st.number_input("会议时长（分钟）", min_value=15, value=30)
        if st.button("查询"):
            booking_prompt = f"根据{attendees}位与会者和{duration}分钟的会议时长，推荐一个合适的会议室。"
            try:
                messages = [HumanMessage(content=booking_prompt)]

                with st.spinner('正在查询会议室...'):
                    booking_result = st.session_state.receptionist_agent.graph.invoke({'messages': messages})

                st.success(booking_result['messages'][-1].content)

            except Exception as e:
                st.error(f'Error finding a meeting room: {e}')


def render_knowledge_base():
    st.title("企业内部知识库")
    st.write("欢迎使用企业内部知识库。请输入您的问题。")

    user_input = st.text_input(
        '您的问题',
        key='kb_query',
        placeholder='例如：“如何申请报销？”',
    )

    if st.button('查询 '):
        if user_input:
            try:
                messages = [HumanMessage(content=user_input)]

                with st.spinner('正在查询答案...'):
                    kb_result = st.session_state.knowledge_base_agent.graph.invoke({'messages': messages})

                st.markdown(kb_result['messages'][-1].content)

            except Exception as e:
                st.error(f'Error querying knowledge base: {e}')
        else:
            st.error('请输入您的问题。')


def main():
    st.set_page_config(layout="wide")
    initialize_agents()

    st.sidebar.title("导航")
    page = st.sidebar.radio("选择一个功能", ["AI差旅助手", "AI接待", "企业内部知识库"])

    if page == "AI差旅助手":
        render_travel_assistant()
    elif page == "AI接待":
        render_receptionist()
    elif page == "企业内部知识库":
        render_knowledge_base()


if __name__ == '__main__':
    main()