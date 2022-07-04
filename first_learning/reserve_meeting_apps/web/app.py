import streamlit as st
import datetime 
import random
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])



if page == 'users':
    
    st.title('ユーザー登録画面')

    with st.form(key='user'):
        username: str = st.text_input('ユーザ名', max_chars=12)
        data = {'username': username}

        submit_button = st.form_submit_button(label='送信')
        
        if submit_button:
            st.write('## レスポンス結果')

            url = 'http://api:8082/users'
            res = requests.post(url, data=json.dumps(data))
            if res.status_code == 200:
                st.success('ユーザー登録が完了しました')
            else:
                st.error('ユーザー登録に失敗しました')
            st.write(res.status_code)
            st.json(res.json())

elif page == 'rooms':
    st.title('会議室登録画面')

    with st.form(key='room'):
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        
        data = {
            'room_name': room_name,
            'capacity': capacity
        }

        submit_button = st.form_submit_button(label='送信')
        
        if submit_button:
            st.write('## レスポンス結果')
            
            url = 'http://api:8082/rooms'
            res = requests.post(url, data=json.dumps(data))
            if res.status_code == 200:
                st.success('登録が完了しました')
            else:
                st.error('登録に失敗しました')
            st.write(res.status_code)
            st.json(res.json())

else:
    st.title('会議室予約画面')

    # ユーザー取得
    url_users = 'http://api:8082/users'
    res = requests.get(url_users)
    users = res.json()
    users_name = {}
    for user in users:
        users_name[user['username']] = user['user_id']
    
    # 会議室取得
    url_rooms = 'http://api:8082/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
    # rooms_name = [{room['room_name']: {'room_id': room['room_id'], 'capacity': room['capacity']}} for room in rooms]
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'], 
            'capacity': room['capacity']
        }

    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)
    
    # 会議室一覧
    st.write('### 予約一覧')
    url_bookings = 'http://api:8082/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)
    
    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['username']
    
    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity':  room['capacity']
        }
    
    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]['room_name']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')
    
    df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)
    df_bookings = df_bookings.rename(columns={
        'user_id': '予約者名', 
        'room_id': '予約会議室名',
        'booked_num': '予約人数',
        'start_datetime': '開始時刻',
        'end_datetime': '終了時刻',
        'booking_id': '予約番号',
    })
    
    st.table(df_bookings)

    with st.form(key='booking'):
        username: str = st.selectbox('予約者名', users_name)
        room_name: str = st.selectbox('会議室名', rooms_name.keys())
        booked_num: int = st.number_input('予約人数', step=1)
        date = st.date_input('日付: ', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻: ', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('終了時刻: ', value=datetime.time(hour=20, minute=0))


        submit_button = st.form_submit_button(label='送信')
        
        if submit_button:
            user_id: int = users_name[username]
            room_id: int = rooms_name[room_name]['room_id']
            capacity: int = rooms_name[room_name]['capacity']
            
            data = {
                'user_id': user_id,
                'room_id': room_id,
                'booked_num': booked_num,
                'start_datetime': datetime.datetime(
                                    year=date.year, 
                                    month=date.month, 
                                    day=date.day,
                                    hour=start_time.hour,
                                    minute=start_time.minute
                                ).isoformat(),
                'end_datetime': datetime.datetime(
                                    year=date.year, 
                                    month=date.month, 
                                    day=date.day,
                                    hour=end_time.hour,
                                    minute=end_time.minute
                                ).isoformat()
            }
            
            #  予約人数の場合
            if booked_num > capacity:
                st.error(f'{room_name}の定員は、{capacity}名です')
            
            # 開始時刻 >= 終了時刻
            elif start_time >= end_time:
                st.error(f'開始時刻が終了時刻を超えています。')
            elif start_time < datetime.time(hour=9, minute=0) or end_time > datetime.time(hour=20, minute=0):
                st.error(f'利用時間は9 ~ 20時の間です')
            else:
                # 会議室の予約を行う
                
                url = 'http://api:8082/bookings'
                res = requests.post(url, data=json.dumps(data))

                if res.status_code == 200:
                    st.success('予約が完了しました')
                elif res.status_code == 404:
                    if 'detail' in res.json().keys():
                        st.write(res.json()['detail'])