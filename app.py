

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