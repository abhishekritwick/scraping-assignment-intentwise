import os
PATH = "{}/chromedriver".format(str(os.getcwd()))
FILENAME = 'testdata.html'

xpath_dict = {
    'search_results':'[data-component-type=s-search-results] .s-result-list > .s-result-item[data-component-type=s-search-result],\
        ._multi-card-creative-desktop_DesktopGridColumn_gridColumn__2evuV,\
        .sbx_mcd div[data-asin]',
    'keyword':'.sg-row-align-items-center .sg-col-14-of-20 .sg-col-inner .a-text-bold',
    'rank':'',
    'product_url':'h2>a.a-link-normal.a-text-normal',
    'asin':'[data-asin]',
    'prod_desc':'h2>a.a-link-normal.a-text-normal span,.a-truncate-full.a-offscreen,[data-click-el=title]', 
    'seller_company':'h2>a.a-link-normal.a-text-normal span,.a-truncate-full.a-offscreen,[data-click-el=title]',
    'strike_price':'.a-price[data-a-strike=true] .a-offscreen', 
    'display_price':'.a-price[data-a-color=price] .a-offscreen',
    'rating_count':'.a-spacing-top-micro .a-row.a-size-small span:nth-of-type(2)[aria-label]',
    'five_rating':'.a-spacing-top-micro .a-row.a-size-small span:nth-of-type(1)[aria-label],.a-icon.a-icon-star.a-star-4-5+span',
    'badge':'.a-row.a-badge-region .a-badge-text',
    'sponsored':'.s-label-popover-hover>span',
}