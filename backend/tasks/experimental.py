import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('project.db')

# Query to fetch show ratings
query = "SELECT rating, COUNT(*) as count FROM show GROUP BY rating"
ratings_data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(ratings_data['rating'], ratings_data['count'])
plt.xlabel('Show Rating')
plt.ylabel('Number of Shows')
plt.title('Distribution of Show Ratings')
plt.show()


import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('project.db')

# Query to fetch ticket quantities
query = "SELECT quantity FROM ticket"
ticket_data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(ticket_data['quantity'], bins=20, edgecolor='k')
plt.xlabel('Ticket Quantity')
plt.ylabel('Frequency')
plt.title('Distribution of Ticket Quantities')
plt.show()


import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('project.db')

# Query to fetch ticket price and show ratings
query = "SELECT ticket_price, rating FROM show"
scatter_data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(scatter_data['ticket_price'], scatter_data['rating'])
plt.xlabel('Ticket Price')
plt.ylabel('Show Rating')
plt.title('Ticket Price vs. Show Rating')
plt.show()


