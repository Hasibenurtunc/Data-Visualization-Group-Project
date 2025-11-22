

# VISUALIZATION 1: PIE CHART - Sales Distribution by Category
st.header("1. Pie Chart - Sales Distribution by Category")
col1, col2 = st.columns([3, 1])

with col1:
    category_sales = final_filtered_df.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    
    fig3 = px.pie(
        category_sales,
        values='Purchase Amount (USD)',
        names='Category',
        title='Sales Distribution by Category',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("**Select Categories:**")
    category_list = df['Category'].unique().tolist()
    
    new_cat_selection = []
    
    for cat in category_list:
        if st.checkbox(cat, value=cat in st.session_state.selected_categories, 
                      key=f'cat_checkbox_{cat}_{st.session_state.checkbox_reset_counter}'):
            new_cat_selection.append(cat)
    
    if set(new_cat_selection) != set(st.session_state.selected_categories):
        st.session_state.selected_categories = new_cat_selection
        st.rerun()
    
    if st.button("Clear Categories", key='clear_cat', use_container_width=True):
        st.session_state.selected_categories = []
        st.session_state.checkbox_reset_counter += 1
        st.rerun()

with st.expander("View Insights - Pie Chart"):
    st.write("""
    **Purpose:** Shows the proportion of total sales contributed by each product category
    
    **Insight:** Reveals which categories dominate the revenue stream
    
    **Business Value:** Guides resource allocation and category-specific strategies
    """)

st.markdown("---")

# VISUALIZATION 2: TREEMAP - Sales Hierarchy
st.header("2. Treemap - Sales Hierarchy")
if len(final_filtered_df) > 0:
    treemap_data = final_filtered_df.groupby(['Category', 'Item Purchased'])['Purchase Amount (USD)'].sum().reset_index()
    
    fig4 = px.treemap(
        treemap_data,
        path=['Category', 'Item Purchased'],
        values='Purchase Amount (USD)',
        color='Purchase Amount (USD)',
        color_continuous_scale='Blues',
        title='Category to Item Hierarchy (Hover for details)'
    )
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Insufficient data for Treemap.")

with st.expander("View Insights - Treemap"):
    st.write("""
    **Purpose:** Hierarchical view of sales by category and individual items
    
    **Insight:** Larger rectangles indicate higher sales volume, allowing quick visual comparison
    
    **Business Value:** Identifies top-performing products within each category for strategic stocking
    """)

st.markdown("---")

# VISUALIZATION 3: CORRELATION HEATMAP - Numerical Variables
st.header("3. Correlation Heatmap - Numerical Variables")

numeric_cols = ['Age', 'Purchase Amount (USD)', 'Review Rating', 'Previous Purchases']

if len(final_filtered_df) > 1:
    correlation_data = final_filtered_df[numeric_cols].corr()
    
    fig9, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        correlation_data, 
        annot=True, 
        fmt='.2f',
        cmap='RdBu_r', 
        center=0, 
        square=True, 
        linewidths=1,
        vmin=-1, 
        vmax=1,
        cbar_kws={'label': 'Correlation Coefficient'}
    )
    plt.title('Correlation Matrix of Numerical Variables', fontsize=16, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig9)
    plt.close()
else:
    st.info("Insufficient data for Correlation Heatmap.")

with st.expander("View Insights - Correlation Heatmap"):
    st.write("""
    **Purpose:** Shows statistical correlations between all numerical variables in the dataset
    
    **Insight:** Values close to 1 or -1 indicate strong positive or negative relationships
    
    **Business Value:** Helps understand which factors most strongly influence purchase behavior
    """)

st.markdown("---")

# VISUALIZATION 4: LINE CHART - Average Purchase by Age Group
st.header("4. Line Chart - Average Purchase by Age Group")
col1, col2 = st.columns([3, 1])

with col1:
    filtered_df_temp = final_filtered_df.copy()
    filtered_df_temp['Age Group'] = pd.cut(
        filtered_df_temp['Age'], 
        bins=[0, 25, 35, 45, 55, 65, 100], 
        labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    )
    age_spending = filtered_df_temp.groupby('Age Group', observed=True)['Purchase Amount (USD)'].mean().reset_index()
    
    age_order = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    age_spending['Age Group'] = pd.Categorical(age_spending['Age Group'], categories=age_order, ordered=True)
    age_spending = age_spending.sort_values('Age Group')
    
    fig2 = px.line(
        age_spending,
        x='Age Group',
        y='Purchase Amount (USD)',
        title='Average Purchase Amount by Age Group',
        markers=True,
        line_shape='linear'
    )
    fig2.update_traces(line=dict(color='#059669', width=3), marker=dict(size=12))
    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("**Select Age Groups:**")
    age_group_list = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    
    new_age_selection = []
    
    for age_grp in age_group_list:
        if st.checkbox(age_grp, value=age_grp in st.session_state.selected_age_group, 
                      key=f'age_checkbox_{age_grp}_{st.session_state.checkbox_reset_counter}'):
            new_age_selection.append(age_grp)
    
    if set(new_age_selection) != set(st.session_state.selected_age_group):
        st.session_state.selected_age_group = new_age_selection
        st.rerun()
    
    if st.button("Clear Age Groups", key='clear_age', use_container_width=True):
        st.session_state.selected_age_group = []
        st.session_state.checkbox_reset_counter += 1
        st.rerun()

with st.expander("View Insights - Line Chart"):
    st.write("""
    **Purpose:** Displays average spending patterns across different age groups
    
    **Insight:** Shows which age demographic spends the most on average
    
    **Business Value:** Enables targeted marketing campaigns for high-value age segments
    """)

st.markdown("---")

# VISUALIZATION 5: PARALLEL COORDINATES - Customer Segmentation
st.header("5. Parallel Coordinates Plot - Customer Segmentation")

sample_size = min(500, len(final_filtered_df))
if sample_size >= 2:
    parallel_df = final_filtered_df[['Age', 'Purchase Amount (USD)', 'Review Rating', 'Previous Purchases']].sample(sample_size)
    
    fig6 = px.parallel_coordinates(
        parallel_df,
        dimensions=['Age', 'Purchase Amount (USD)', 'Review Rating', 'Previous Purchases'],
        color='Purchase Amount (USD)',
        color_continuous_scale='Viridis',
        title='Multi-dimensional Customer Profile (Drag axes to reorder)'
    )
    fig6.update_layout(height=500)
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.info("Insufficient data for Parallel Coordinates Plot.")

with st.expander("View Insights - Parallel Coordinates"):
    st.write("""
    **Purpose:** Shows relationships between multiple numerical variables simultaneously
    
    **Insight:** Each line represents an individual customer across different dimensions
    
    **Business Value:** Identifies patterns and segments of high-value customers for targeted engagement
    """)

st.markdown("---")

# VISUALIZATION 6: SUNBURST - Seasonal Category Breakdown
st.header("6. Sunburst Chart - Seasonal Category Breakdown")

if len(final_filtered_df) > 0 and len(final_filtered_df['Season'].unique()) > 1:
    sunburst_data = final_filtered_df.groupby(['Season', 'Category', 'Item Purchased'])['Purchase Amount (USD)'].sum().reset_index()
    
    fig7 = px.sunburst(
        sunburst_data,
        path=['Season', 'Category', 'Item Purchased'],
        values='Purchase Amount (USD)',
        color='Purchase Amount (USD)',
        color_continuous_scale='RdBu_r', 
        title='Season → Category → Item (Click to zoom in)'
    )
    fig7.update_layout(height=600)
    st.plotly_chart(fig7, use_container_width=True)
else:
    st.info("Insufficient data or variety for Sunburst Chart. Need more than one Season.")

with st.expander("View Insights - Sunburst Chart"):
    st.write("""
    **Purpose:** Hierarchical breakdown of sales by season, category, and specific items
    
    **Insight:** Inner rings represent seasons, outer rings show categories and individual products
    
    **Business Value:** Enables seasonal inventory planning and promotional campaign scheduling
    """)

st.markdown("---")

# VISUALIZATION 7: BAR CHART - Top 10 Most Purchased Items
st.header("7. Bar Chart - Top 10 Most Purchased Items")
col1, col2 = st.columns([3, 1])

with col1:
    # Prepare data for bar chart (excluding item filter)
    bar_chart_df = df[
        (df['Gender'].isin(selected_gender)) &
        (df['Season'].isin(selected_season)) &
        (df['Category'].isin(selected_category)) &
        (df['Age'].between(age_range[0], age_range[1])) &
        (df['Purchase Amount (USD)'].between(purchase_range[0], purchase_range[1]))
    ]
    
    # Apply age group filter if exists
    if st.session_state.selected_age_group:
        age_groups_bar = pd.cut(bar_chart_df['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                            labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        bar_chart_df = bar_chart_df[age_groups_bar.isin(st.session_state.selected_age_group)]
    
    # Apply category filter if exists
    if st.session_state.selected_categories:
        bar_chart_df = bar_chart_df[bar_chart_df['Category'].isin(st.session_state.selected_categories)]
    
    # Show selected items or top 10
    if st.session_state.selected_items:
        display_df = bar_chart_df[bar_chart_df['Item Purchased'].isin(st.session_state.selected_items)]
        top_items = display_df['Item Purchased'].value_counts().reset_index()
        top_items.columns = ['Item', 'Count']
        chart_title = f'Selected Items ({len(st.session_state.selected_items)} items)'
    else:
        top_items = bar_chart_df['Item Purchased'].value_counts().head(10).reset_index()
        top_items.columns = ['Item', 'Count']
        chart_title = 'Top 10 Most Purchased Items'
    
    fig1 = px.bar(
        top_items,
        x='Item',
        y='Count',
        title=chart_title,
        color='Count',
        color_continuous_scale='Blues',
    )
    fig1.update_layout(height=450, xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("**Select Items:**")
    
    # Prepare checkbox base data
    checkbox_base_df = filtered_df.copy()
    
    if st.session_state.selected_age_group:
        age_groups_cb = pd.cut(checkbox_base_df['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                            labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        checkbox_base_df = checkbox_base_df[age_groups_cb.isin(st.session_state.selected_age_group)]
    
    if st.session_state.selected_categories:
        checkbox_base_df = checkbox_base_df[checkbox_base_df['Category'].isin(st.session_state.selected_categories)]
    
    # Get top 10 items for checkboxes
    if len(checkbox_base_df) > 0:
        top_items_for_cb = checkbox_base_df['Item Purchased'].value_counts().head(10).reset_index()
        top_items_for_cb.columns = ['Item', 'Count']
        top_10_items = top_items_for_cb['Item'].tolist()
    else:
        top_10_items = []
    
    # Track new selection
    new_selection = []
    
    # Checkbox for each item
    for item in top_10_items:
        is_checked = st.checkbox(
            item, 
            value=item in st.session_state.selected_items,
            key=f'item_checkbox_{item}_{st.session_state.checkbox_reset_counter}'
        )
        
        if is_checked:
            new_selection.append(item)
    
    # Update if selection changed
    if set(new_selection) != set(st.session_state.selected_items):
        st.session_state.selected_items = new_selection
        st.rerun()
    
    # Clear button
    if st.button("Clear Items", key='clear_items', use_container_width=True):
        st.session_state.selected_items = []
        st.session_state.checkbox_reset_counter += 1
        st.rerun()

with st.expander("View Insights - Bar Chart"):
    st.write("""
    **Purpose:** Shows the top 10 most purchased items in the dataset
    
    **Insight:** Identifies best-selling products that drive revenue
    
    **Business Value:** Helps with inventory management and stock planning for high-demand items
    """)

st.markdown("---")

# VISUALIZATION 8: SANKEY DIAGRAM - Customer Journey Flow
st.header("8. Sankey Diagram - Customer Journey Flow")

if len(final_filtered_df) > 1 and len(final_filtered_df['Payment Method'].unique()) > 1:
    sankey_df = final_filtered_df.groupby(['Category', 'Payment Method', 'Shipping Type']).size().reset_index(name='count')
    all_labels = list(pd.concat([sankey_df['Category'], sankey_df['Payment Method'], sankey_df['Shipping Type']]).unique())
    label_dict = {label: idx for idx, label in enumerate(all_labels)}
    
    source, target, values = [], [], []
    for _, row in sankey_df.iterrows():
        source.append(label_dict[row['Category']])
        target.append(label_dict[row['Payment Method']])
        values.append(row['count'])
    
    payment_shipping = final_filtered_df.groupby(['Payment Method', 'Shipping Type']).size().reset_index(name='count')
    for _, row in payment_shipping.iterrows():
        source.append(label_dict[row['Payment Method']])
        target.append(label_dict[row['Shipping Type']])
        values.append(row['count'])
    
    if source:
        fig5 = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, label=all_labels, color="lightblue"),
            link=dict(source=source, target=target, value=values)
        )])
        fig5.update_layout(title_text="Category → Payment → Shipping Flow", height=600)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Insufficient linked data for Sankey Diagram.")
else:
    st.info("Insufficient data for Sankey Diagram. Need more varied Payment/Shipping types.")

with st.expander("View Insights - Sankey Diagram"):
    st.write("""
    **Purpose:** Visualizes the customer journey from category selection to payment and shipping preferences
    
    **Insight:** Flow thickness represents transaction volume through each path
    
    **Business Value:** Understands payment and shipping preferences by category to optimize checkout experience
    """)

st.markdown("---")

# VISUALIZATION 9: 3D SCATTER PLOT - Multi-dimensional Analysis with Glyphs
st.header("9. 3D Scatter Plot - Multi-dimensional Analysis with Glyphs")

sample_size_3d = min(1000, len(final_filtered_df))

if sample_size_3d >= 2:
    scatter_3d = final_filtered_df.sample(sample_size_3d)
    
    # Create symbol mapping for payment methods
    symbol_map = {
        'Cash': 'circle',
        'Credit Card': 'diamond',
        'Debit Card': 'cross',
        'PayPal': 'square',
        'Venmo': 'x',
        'Bank Transfer': 'diamond-open'
    }
    
    fig8 = px.scatter_3d(
        scatter_3d,
        x='Age',
        y='Purchase Amount (USD)',
        z='Review Rating',
        color='Category',
        size='Previous Purchases',
        symbol='Payment Method',
        symbol_map=symbol_map,
        hover_data=['Gender', 'Season'],
        title='Age × Purchase × Rating by Payment Method (Rotate to explore)',
        color_discrete_sequence=['#3b82f6', '#ef4444', '#fbbf24', '#10b981'] 
    )
    fig8.update_layout(height=600)
    st.plotly_chart(fig8, use_container_width=True)
else:
    st.info("Insufficient data for 3D Scatter Plot.")

with st.expander("View Insights - 3D Scatter Plot"):
    st.write("""
    **Purpose:** Three-dimensional relationship between age, spending, and customer satisfaction
    
    **Insight:** Point shape (glyph) indicates the Payment Method used. This helps identify if certain payment methods correlate with high review scores or high spending
    
    **Business Value:** Identifies loyal, high-value customer segments based on their preferred payment channels
    """)

st.markdown("---")


# FOOTER
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px; background-color: #f3f4f6; border-radius: 10px;'>
        <h3>Team Members</h3>
        <p><strong>Ceren | Gülse | Hasibe</strong></p>
        <p>CEN445 Data Visualization Project | 2025-26</p>
        <p><strong>3 Basic + 6 Advanced Visualizations</strong> | Business Intelligence Dashboard</p>
    </div>
""", unsafe_allow_html=True)