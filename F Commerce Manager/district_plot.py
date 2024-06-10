import pandas as pd
import matplotlib.pyplot as plt


districts = [
    'Dhaka', 'Faridpur', 'Gazipur', 'Gopalganj', 'Jamalpur', 'Kishoreganj', 'Madaripur', 'Manikganj', 'Munshiganj', 'Mymensingh',
    'Narayanganj', 'Narsingdi', 'Netrokona', 'Rajbari', 'Shariatpur', 'Sherpur', 'Tangail', 'Bogra', 'Joypurhat', 'Naogaon',
    'Natore', 'Nawabganj', 'Pabna', 'Rajshahi', 'Sirajgonj', 'Dinajpur', 'Gaibandha', 'Kurigram', 'Lalmonirhat', 'Nilphamari',
    'Panchagarh', 'Rangpur', 'Thakurgaon', 'Barguna', 'Barisal', 'Bhola', 'Jhalokati', 'Patuakhali', 'Pirojpur', 'Bandarban',
    'Brahmanbaria', 'Chandpur', 'Chittagong', 'Comilla', "Cox's Bazar", 'Feni', 'Khagrachari', 'Lakshmipur', 'Noakhali', 'Rangamati',
    'Habiganj', 'Maulvibazar', 'Sunamganj', 'Sylhet', 'Bagerhat', 'Chuadanga', 'Jessore', 'Jhenaidah', 'Khulna', 'Kushtia', 'Magura',
    'Meherpur', 'Narail', 'Satkhira'
]


def validate_district(district):
    return district in districts

order_sheet_file = "orders.csv"
order_data = pd.read_csv(order_sheet_file)
order_data = order_data[order_data['District'].apply(validate_district)]
district_counts = order_data['District'].value_counts(normalize=True) * 100
top_20_districts = district_counts.head(20)
other_percentage = district_counts.iloc[20:].sum()
top_20_districts.loc["Other"] = other_percentage


plt.figure(figsize=(10, 8))
plt.pie(top_20_districts, labels=top_20_districts.index + ' (' + top_20_districts.map('{:.1f}%'.format) + ')', autopct='%1.1f%%', startangle=140)
plt.title('Top 20 Districts Order Count Percentage')
plt.axis('equal')
plt.show()
