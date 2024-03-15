from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

SPREADSHEET_BODY_TEMPLATE = {
    'properties': {
        'title': '',
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }
    ]
}

async def generate_spreadsheet_body(now_date_time: str) -> dict:
    spreadsheet_body = SPREADSHEET_BODY_TEMPLATE.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт на {now_date_time}'
    return spreadsheet_body


async def generate_table_values(now_date_time: str) -> list:
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=generate_spreadsheet_body(now_date_time))
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = generate_table_values(now_date_time)
    for charity_project in charity_projects:
        new_row = [
            str(charity_project.name),
            str(charity_project.days_to_complete),
            str(charity_project.description)
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    number_of_row = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{number_of_row}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
