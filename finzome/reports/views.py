from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import math


class UploadCSV(APIView):
    def post(self, request):
        file_obj = request.data.get('file')
        if not file_obj:
            return Response('Please upload file to process', status=status.HTTP_400_BAD_REQUEST)
        df = pd.read_csv(file_obj)

        # determining daily returns
        column_name = 'Close '
        daily_returns = []
        for index in range(1, len(df)):
            current_close = df.iloc[index][column_name]
            previous_close = df.iloc[index-1][column_name]
            current_returns = current_close/previous_close - 1
            daily_returns.append(current_returns)

        # determining daily volatility
        daily_returns_df = pd.DataFrame(daily_returns)
        daily_volatility = daily_returns_df[0].std()

        # determine annualized volatility
        annualized_volatility = daily_volatility * math.sqrt(len(df))

        response = {
            'daily_volatility': daily_volatility,
            'annualized_volatility': annualized_volatility
        }

        return Response(response, status=status.HTTP_200_OK)