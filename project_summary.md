# 📦 Project Snapshot
Generated: 2025-04-20 16:03:14

## 📁 Directory Tree
````
/Users/stevencohen/Projects/universal_recycling/orders_project
├── backend
│   ├── __init__.py
│   ├── database.py
│   ├── endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── lookups.py
│   │   ├── orders.py
│   │   ├── requesters.py
│   │   ├── supplier_lookup.py
│   │   ├── supplier_lookup_takealot.py
│   │   └── ui_pages.py
│   ├── main.py
│   ├── scrapers
│   └── utils
│       ├── __init__.py
│       └── order_utils.py
├── builder_dump.html
├── data
│   ├── orders.db
│   ├── printouts
│   │   ├── order_1.txt
│   │   ├── order_3.txt
│   │   └── order_7.txt
│   ├── test_orders.db
│   └── uploads
│       ├── 20_test_invoice.pdf
│       ├── 21_test_invoice.pdf
│       └── test_invoice.pdf
├── frontend
│   ├── static
│   │   ├── css
│   │   └── js
│   └── templates
│       ├── audit.html
│       ├── home.html
│       ├── index.html
│       ├── login.html
│       ├── maintenance.html
│       ├── new_order.html
│       ├── pending_orders.html
│       ├── print_template.html
│       └── received.html
├── logs
│   ├── db_activity_log.txt
│   ├── lookups_log.txt
│   ├── new_orders_log.txt
│   ├── server.log
│   ├── server_startup.log
│   ├── supplier_lookup_debug.log
│   ├── takealot_lookup.log
│   └── testing_log.txt
├── project_status_snapshot.md
├── project_summary.md
└── scripts
    ├── add_debug_validation_handler.py
    ├── clear_live_data.py
    ├── dump_project_summary.py
    ├── git_pull_project.py
    ├── git_push_project.py
    ├── init_db_fresh.py
    ├── inject_filter_route.py
    ├── insert_get_all_orders.py
    ├── insert_next_order_number_route.py
    ├── insert_pending_route.py
    ├── insert_print_route.py
    ├── insert_receive_route.py
    ├── integration_tests.py
    ├── prepare_lookup_tables.py
    ├── repair_orders_routes.py
    ├── reset_and_test.sh
    ├── seed_static_data.py
    ├── start_server.py
    ├── test_authorisation_threshold_trigger.py
    ├── test_invalid_data_handling.py
    ├── test_invalid_items_variants.py
    ├── test_pipeline_end_to_end.py
    └── test_receive_partial.py
````
## 📄 Source Files

### `.DS_Store`
**(No description)**
```python
<!-- ERROR reading .DS_Store: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte -->
```

### `builder_dump.html`
**(No description)**
```python
<!DOCTYPE html>
<html lang=en data-appversion=v0.0.1578><head><link href="//accounts.google.com" rel=dns-prefetch /><title>Builders | Shop DIY, Paint and Building Materials Online</title><meta charset=utf-8 /><meta content="initial-scale=1,width=device-width,interactive-widget=resizes-content" name=viewport /><script>var __ZBE__={"uh":"aHR0cHM6Ly93d3cuYnVpbGRlcnMuY28uemE","sc":"R2g2dHVjNkw","ic":"YnVpbGRlcnM","mg":"QUl6YVN5QlI5SzVyZUFNTl9CcFFmbzBBczBfb1UwUWVEWWZpYXdv","icf":"MjU5MjU2MTgyMDIwODM2","ica":"Y28uemEuYnVpbGRlcnMubG9naW4","icg":"MzkzNDAxOTkwODY2LTFrOTBwcWIwamVlM2h1dmhpZWIybnJudjgwdTFiYjJjLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29t",};window.__ZBE__=__ZBE__;</script><link rel=dns-prefetch href="https://www.googletagmanager.com"/><link rel=dns-prefetch href="https://apps.bazaarvoice.com"/><link rel=dns-prefetch href="https://www.google-analytics.com"/><link rel=dns-prefetch href="https://www.googleoptimize.com"/><link rel=dns-prefetch href="https://maps.googleapis.com"/><script>var userType="",loginStatus="",dataLayer=[{user_type:userType,logged_in_status:loginStatus}];!function(e,t,a,s,n){e[s]=e[s]||[],e[s].push({"gtm.start":(new Date).getTime(),event:"gtm.js"});var r=t.getElementsByTagName(a)[0],g=t.createElement(a);g.async=!0,g.src="https://www.googletagmanager.com/gtm.js?id=GTM-PCPNHSJ",r.parentNode.insertBefore(g,r)}(window,document,"script","dataLayer")</script><script>window._pxAppId='PXBIA59zcf'</script><script async=async defer=defer src="/px/PXBIA59zcf/init.js"></script><style>body,html{height:100%}body{background-color:#fff;font-family:sans-serif}@font-face {src:url(/Roboto-Regular.woff2);font-family:Roboto;font-weight:400;font-display:swap}@font-face {src:url(/Roboto-Medium.ttf);font-family:Roboto;font-weight:500;font-display:swap}@font-face {src:url(/Roboto-Bold.woff2);font-family:Roboto;font-weight:700;font-display:swap}#react-app{display:flex;height:100%;overflow:hidden}.pac-container{z-index:99999999999;position:fixed!important;margin-bottom:8px}.pac-container:after{content:none!important}.pac-item{padding:5px 4px 5px}.FSs{font-size:14px;font-weight:400;font-family:Roboto;line-height:20px;letter-spacing:.2px;color:#222223}.nav-links-container{display:flex}.mobile-header{display:none}.header,.mobile-header{position:sticky;top:0;background-color:#ffd600;z-index:2}.mobile-header{padding-top:12px}.header .header-container{display:flex;flex-direction:column;flex:1;margin:auto}.header .search-max-container{max-width:1440px;margin-left:auto;margin-right:auto;padding-left:24px;padding-right:24px}.header .menu-inner-container,.header .search-inner-container,.header .search-max-container{box-sizing:border-box;display:flex;justify-content:space-between;align-items:center}.header .logo{display:inline-flex;padding-bottom:5px}.header .action-container{display:flex;justify-content:space-between}.menu-toggler{background-color:transparent;color:#222223;border:none;font-size:16px;font-family:Roboto;line-height:24px;letter-spacing:.2px;padding:0;display:flex;align-items:center;cursor:pointer;font-weight:500}.header .deals-menu-toggler{background-color:transparent;border:none;cursor:pointer;padding:0}.header .action-container{box-sizing:border-box}.header .nav-link{text-decoration:none}.header .menu-container{background-color:#ffeb80;padding-top:6px;padding-bottom:6px}.header .menu-inner-container{max-width:1440px;margin-left:auto;margin-right:auto;padding-left:24px;padding-right:24px}.header .search-bar-container,.mobile-header .search-bar-container{display:flex;margin-left:24px;flex:1 1 0%;min-width:220px;position:relative;border-radius:32px;overflow:hidden;width:100%;border:1px solid #ffd600;padding:0;height:44px;box-sizing:border-box}.search-input-bar{font-family:Roboto;letter-spacing:.2px}.search-input-bar::-ms-input-placeholder,.search-input-bar::placeholder{font-family:Roboto;color:#74767c}.header .search-bar-container>input,.mobile-header .search-bar-container>input{outline-style:none;color:#333;font-size:16px;background-color:#fff;border-bottom-left-radius:32px;border-top-left-radius:32px;padding:16px 16px 15px 24px;border:none;width:100%}.header .search-btn-container,.mobile-header .search-btn-container{display:flex;align-items:center;background-color:#fff;align-items:center;justify-content:center;border-bottom-right-radius:34px;border-top-right-radius:34px}.header .search-btn-container>div,.mobile-header .search-btn-container>div{width:34px;height:34px;align-items:center;justify-content:center;border-radius:16px;margin:4px;background-color:#0d5dfe;display:flex}.desktop-location-container{display:flex;align-items:center}.btn-container{display:flex;padding-left:8px;padding-right:12px;margin-left:24px;border-radius:8px;height:40px;text-decoration:none}.btn-container__text{margin-left:6px}.btn-container:active,.btn-container:hover{background-color:#febc00}.cart__icon-wrapper{margin-left:24px;padding-left:12px}.header .search-bar-container{margin-left:24px}.header .sign-in-text{max-width:95px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.location-link-text{padding-left:4px;padding-right:71px}.desktop-link-text{text-decoration:none;margin-left:24px}#mobile-default-header,#web-default-header{position:absolute;top:0;left:0;right:0}.header .nav-links-container .buy-again-toggler{opacity:0;font-weight:400;font-size:14px;line-height:20px}@media only screen and (max-width:1024px){.header{display:none!important}.mobile-header{display:block;padding-top:0}.mobile-header .header-container{padding-top:0}.mobile-header .left,.mobile-header .right{display:flex;align-items:center}.mobile-header .right{justify-content:right}.mobile-header .search-bar-container{margin-left:0;max-width:100%;height:48px;padding:0 16px 8px 16px}.mobile-header .search-bar-container>input{padding:16px 16px 15px 16px}.mobile-header .search-btn-container{width:48px}.mobile-header .mobile-location-container{display:flex;flex-direction:row;justify-content:space-between;background-color:#ffeb80;align-items:center;padding:6px 16px}.mobile-header .mobile-deliver-text{flex:1 1 0%;margin:0;padding-right:12px;padding-left:4px}.mobile-header .search-btn-container>div{margin:2px}.mobile-header .logo-container{padding-left:16px;padding-right:16px;display:flex;justify-content:space-between;align-items:center}.hamburger-mobile-icon{display:flex;margin-top:4px;margin-right:16px}.mobile-header .logo{display:inline-flex;margin-bottom:10px}.mobile-header .cart__icon-wrapper:active{background-color:transparent}}</style><style>body{margin:0}#loader-wrapper{width:100%;display:flex;justify-content:center;align-items:center;background-color:#fff;margin-top:104px}#ctn{display:flex;flex-direction:column;justify-content:center;align-items:center}#loader{width:20px;height:20px;animation:rotate 1s infinite ease}#loader-text{text-align:center;color:#222223;font-family:Roboto;font-size:16px;line-height:24px;letter-spacing:.2px;margin-top:10px}@keyframes rotate{0%{transform:none}100%{transform:rotate(1turn)}}</style></head><body><header id=web-default-header style="display:flex;flex:1 1 0%;overflow:hidden" class=header><div class=header-container><div class=search-container><div class=search-max-container><div class=search-inner-container><a href="/" class=logo data-testid=headerLogo><svg width=70 height=67 viewBox="0 0 70 67" fill=none xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#a)"><path d=M3-2H1v68h68V-2H3z fill="#FFD600" stroke="#fff" stroke-width=4></path><path d="M37.425 27.207h3.536v4.425l10.063 6.686h-5.24l-13.5-8.6-13.513 8.6h-5.24l18.753-12.48 5.14 3.43v-2.061z" fill="#fff"></path><path d="M12.605 42.035a.514.514 0 0 1 .12-.379.487.487 0 0 1 .358-.12c.323 0 .486.174.486.52v7.015a.59.59 0 0 1-.122.397.605.605 0 0 1-.723 0 .59.59 0 0 1-.12-.397v-7.035zm0-4.831H9.83l-.02.011v13.971h2.108l.244-.386.504.339c.357.15.742.218 1.128.2.818 0 1.468-.205 1.951-.618a1.612 1.612 0 0 0 .623-1.24v-8.127a1.383 1.383 0 0 0-.582-1.13 2.212 2.212 0 0 0-1.447-.45 4.837 4.837 0 0 0-1.046.1 1.61 1.61 0 0 0-.677.321l-.011-2.991zm44.144 9.426h-2.793v2.418c0 .85.329 1.463.985 1.838.535.307 1.287.452 2.258.452.97 0 1.77-.174 2.332-.522.655-.397.982-1.024.982-1.878v-1.696a2.032 2.032 0 0 0-.58-1.538c-.187-.188-.676-.489-1.468-.903l-1.086-.578a1.207 1.207 0 0 1-.6-1.079v-1.059a.564.564 0 0 1 .14-.42.47.47 0 0 1 .34-.14.418.418 0 0 1 .321.163.529.529 0 0 1 .142.397v2.217h2.732v-2.237c0-.851-.316-1.463-.941-1.836-.526-.307-1.271-.451-2.235-.451s-1.761.174-2.31.519c-.628.402-.942 1.028-.942 1.878v1.52c-.027.44.093.876.341 1.24.383.395.832.72 1.328.957.452.24.917.494 1.427.76.361.227.54.725.54 1.498v.878a.722.722 0 0 1-.118.44.37.37 0 0 1-.323.142.418.418 0 0 1-.34-.142.709.709 0 0 1-.123-.44l-.009-2.398zm-6.773-6.773h-2.8v11.327h2.786v-9.108a.502.502 0 0 1 .122-.377.487.487 0 0 1 .364-.122c.318 0 .48.174.48.52v2.458h2.794v-3.16a1.392 1.392 0 0 0-.583-1.13 2.159 2.159 0 0 0-1.445-.48 3.641 3.641 0 0 0-1.047.14c-.246.059-.477.169-.678.322l.007-.39zm-7.478 2.237a.567.567 0 0 1 .14-.42.506.506 0 0 1 .705 0 .64.64 0 0 1 .117.42v2.61h-.962v-2.61zm-2.793.08v6.773c0 .867.32 1.5.962 1.898.537.335 1.302.502 2.294.502.989 0 1.754-.154 2.287-.452a1.97 1.97 0 0 0 1.007-1.838V46.75h-2.802v2.28a.72.72 0 0 1-.117.438.451.451 0 0 1-.366.142.45.45 0 0 1-.361-.142.72.72 0 0 1-.118-.438v-2.637h3.757v-4.317c0-.851-.338-1.463-1.007-1.836-.55-.3-1.312-.451-2.287-.451-.975 0-1.746.173-2.312.52-.63.401-.944 1.027-.944 1.878l.007-.014zm-4.694-.107c0-.345.158-.52.481-.52a.432.432 0 0 1 .341.14.452.452 0 0 1 .142.36v7.035a.6.6 0 0 1-.122.398.498.498 0 0 1-.361.12.488.488 0 0 1-.361-.12.59.59 0 0 1-.12-.398v-7.015zm-2.795-.698v8.129a1.663 1.663 0 0 0 .661 1.298c.452.375 1.095.56 1.91.56a2.71 2.71 0 0 0 1.145-.201c.168-.11.33-.227.483-.355l.24.38h2.113V37.204h-2.793V40.2a2.062 2.062 0 0 0-.706-.3 4.1 4.1 0 0 0-1.023-.122 2.258 2.258 0 0 0-1.468.451 1.396 1.396 0 0 0-.562 1.13v.01zm-.928-4.167h-2.795v13.984h2.795V37.202zm-3.723 2.655H24.77v11.33h2.795v-11.33zm0-2.653H24.77v2.032h2.795v-2.032zm-7.48 2.655H17.29v9.907a1.4 1.4 0 0 0 .562 1.13c.423.312.941.472 1.467.45.355.008.709-.047 1.046-.16a1.83 1.83 0 0 0 .677-.379v.38h2.8V39.858h-2.793v9.23a.556.556 0 0 1-.122.38.498.498 0 0 1-.361.119c-.323 0-.481-.174-.481-.517v-9.212zm42.973 12.747H6.944v-13.48l2.87-1.918v-.011h.02l22.504-15.026 2.935 1.951h8.58v5.726l9.708 6.482h9.497v16.276zm.677-16.933h-9.97l-9.258-6.168v-6.047h-9.053l-3.13-2.09-26.06 17.405v14.51h57.471v-17.61z" fill="#231F20"></path></g><path stroke="#fff" stroke-width=3 d=M1.5-1.5h67v67h-67z></path><defs><clipPath id=a><path fill="#fff" d="M3 0h64v64H3z"></path></clipPath></defs></svg> </a><button type=button class="btn-container menu-toggler"><svg width=16 height=16 viewBox="0 0 14 15" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M5.95039 7.80582C6.16813 7.80582 6.34698 7.97282 6.36618 8.1856L6.36789 8.2236V13.7005C6.36789 13.9183 6.20114 14.0971 5.98838 14.1163L5.95039 14.118H0.473442C0.255695 14.118 0.0766004 13.9513 0.057373 13.7385L0.0556641 13.7005V8.2236C0.0556641 8.00585 0.222662 7.82676 0.435442 7.80753L0.473442 7.80582H5.95039ZM13.5432 7.80582C13.7609 7.80582 13.9398 7.97282 13.959 8.1856L13.9607 8.2236V13.7005C13.9607 13.9183 13.7939 14.0971 13.5812 14.1163L13.5432 14.118H8.069C7.85099 14.118 7.67213 13.9513 7.65293 13.7385L7.65122 13.7005V8.2236C7.65122 8.00585 7.81797 7.82676 8.03096 7.80753L8.069 7.80582H13.5432ZM5.53261 8.64138H0.89122V13.2828H5.53261V8.64138ZM13.1254 8.64138H8.48678V13.2828H13.1254V8.64138ZM5.95039 0.055542C6.16813 0.055542 6.34698 0.22254 6.36618 0.43532L6.36789 0.47332V5.95027C6.36789 6.16801 6.20114 6.34711 5.98838 6.36633L5.95039 6.36804H0.473442C0.255695 6.36804 0.0766004 6.20105 0.057373 5.98827L0.0556641 5.95027V0.47332C0.0556641 0.255573 0.222662 0.0764783 0.435442 0.0572509L0.473442 0.055542H5.95039ZM13.5432 0.055542C13.7609 0.055542 13.9398 0.22254 13.959 0.43532L13.9607 0.47332V5.95027C13.9607 6.16801 13.7939 6.34711 13.5812 6.36633L13.5432 6.36804H8.069C7.85099 6.36804 7.67213 6.20105 7.65293 5.98827L7.65122 5.95027V0.47332C7.65122 0.255573 7.81797 0.0764783 8.03096 0.0572509L8.069 0.055542H13.5432ZM5.53261 0.891098H0.89122V5.53249H5.53261V0.891098ZM13.1254 0.891098H8.48678V5.53249H13.1254V0.891098Z" fill=black></path></svg><div dir=auto class=btn-container__text>Shop by Department</div></button></div><div class=search-bar-container><input placeholder="What can we help you find?" maxlength=100 autocapitalize=sentences autocomplete=on autocorrect=on dir=auto enterkeyhint=search spellcheck=true class=search-input-bar data-testid=searchInputField value=""/><div class=search-btn-container><div aria-disabled=true aria-label=Search role=button tabindex=-1 class=""><svg width=24 height=24 viewBox="0 0 32 32" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M14 5a9 9 0 017.032 14.617l5.1 5.1a.5.5 0 010 .708l-.707.707a.5.5 0 01-.707 0l-5.1-5.1A9 9 0 1114 5zm0 2a7 7 0 100 14 7 7 0 000-14z" fill="#FFFFFF"></path></svg></div></div></div><div class=action-container><button type=button class="btn-container menu-toggler"><svg width=16 height=16 viewBox="0 0 32 32" color=black><path fill-rule=evenodd clip-rule=evenodd d="M16.599 4.474a7.728 7.728 0 00-1.796 7.278l.05.175-12.56 12.556a1 1 0 000 1.415l3.812 3.81.094.083a1 1 0 001.32-.083l12.565-12.562.177.052A7.733 7.733 0 0029.529 7.07l-.05-.116a1 1 0 00-1.595-.248l-3.007 3-2.113-.465-.465-2.112 3.008-3.005a1 1 0 00-.36-1.646A7.734 7.734 0 0016.8 4.265l-.201.209zM22.357 4l.234.008-2.093 2.093a1 1 0 00-.27.922l.72 3.272a1 1 0 00.762.761l3.273.72.125.02a1 1 0 00.796-.289l2.087-2.085.004.053a5.735 5.735 0 01-7.816 5.593l-.124-.04a1 1 0 00-.946.265L6.811 27.586 4.413 25.19l12.295-12.288a1 1 0 00.224-1.073 5.73 5.73 0 011.282-6.15 5.728 5.728 0 014.143-1.678z" fill=currentColor></path></svg><div dir=auto class=btn-container__text>Services</div></button> <button type=button class="wishlist-btn-container btn-container menu-toggler"><svg width=16 height=16 viewBox="0 0 14 12" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M9.75 0C12.0972 0 14 1.90279 14 4.25C14 7.08333 11.6667 9.66667 6.99998 12C2.33333 9.66667 0 7.08333 0 4.25C0 1.90279 1.90279 0 4.25 0C5.29899 0 6.25922 0.380043 7.00052 1.00995C7.74121 0.379873 8.70124 0 9.75 0ZM9.75 1C9.04599 1 8.3789 1.22356 7.82777 1.6296L7.64846 1.77164L7.00086 2.32253L6.35298 1.77199C5.7694 1.27609 5.03234 1 4.25 1C2.45507 1 1 2.45507 1 4.25C1 6.48587 2.85783 8.66697 6.74089 10.7407L7 10.876L7.25908 10.7407C11.028 8.72796 12.889 6.61408 12.9952 4.44714L13 4.25C13 2.45507 11.5449 1 9.75 1Z" fill=black></path></svg><div class=btn-container__text dir=auto>Wishlist</div></button><div class="btn-container menu-toggler"><svg width=16 height=16 viewBox="0 0 24 24" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M12 1.5C14.8995 1.5 17.25 3.85051 17.25 6.75C17.25 8.23641 16.6323 9.57854 15.6395 10.5337C18.6526 10.8529 21 13.4023 21 16.5V22.5H3V16.5C3 13.4023 5.34744 10.8529 8.36045 10.5337C7.36772 9.57854 6.75 8.23641 6.75 6.75C6.75 3.85051 9.1005 1.5 12 1.5ZM12 12H9C6.58573 12 4.61551 13.9012 4.5049 16.2882L4.5 16.5V21H19.5V16.5C19.5 14.0857 17.5988 12.1155 15.2118 12.0049L15 12H12ZM12 10.5C14.0711 10.5 15.75 8.82107 15.75 6.75C15.75 4.67893 14.0711 3 12 3C9.92893 3 8.25 4.67893 8.25 6.75C8.25 8.82107 9.92893 10.5 12 10.5Z" fill=black></path></svg><div class="btn-container__text sign-in-text" dir=auto>Sign in</div></div><a aria-label=Cart role=button href="/cart" class="btn-container menu-toggler cart__icon-wrapper"><svg width=24 height=24 viewBox="0 0 32 32" fill=none xmlns="http://www.w3.org/2000/svg"><path fill-rule=evenodd clip-rule=evenodd d="M7.99327 4.38338C7.93551 3.88604 7.51284 3.5 7 3.5H3L2.88338 3.50673C2.38604 3.56449 2 3.98716 2 4.5L2.00673 4.61662C2.06449 5.11396 2.48716 5.5 3 5.5H6V20.5L6.00673 20.6166C6.06449 21.114 6.48716 21.5 7 21.5H29L29.1166 21.4933C29.614 21.4355 30 21.0128 30 20.5V8.5L29.9933 8.38338C29.9355 7.88604 29.5128 7.5 29 7.5H8V4.5L7.99327 4.38338ZM8 9.5H28V19.5H8V9.5ZM25.818 25C25.818 26.3807 24.6987 27.5 23.318 27.5C21.9373 27.5 20.818 26.3807 20.818 25C20.818 23.6193 21.9373 22.5 23.318 22.5C24.6987 22.5 25.818 23.6193 25.818 25ZM11.318 27.5C12.6987 27.5 13.818 26.3807 13.818 25C13.818 23.6193 12.6987 22.5 11.318 22.5C9.93728 22.5 8.81799 23.6193 8.81799 25C8.81799 26.3807 9.93728 27.5 11.318 27.5Z" fill=black></path></svg></a></div></div></div><div class=menu-container><div class=menu-inner-container><div class=desktop-location-container><svg width=16 height=16 viewBox="0 0 32 32" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M16 2.03125C21.5228 2.03125 26 6.08268 26 12.0312C26 16.6949 22.6667 22.6758 16 29.9741C9.33333 22.6724 6 16.6915 6 12.0312C6 6.07829 10.4772 2.03125 16 2.03125ZM16 4.03125C11.4154 4.03125 8 7.34513 8 12.0312C8 15.6712 10.5359 20.5782 15.6998 26.6166L16 26.9653L16.3004 26.6171C21.352 20.7125 23.8885 15.8882 23.9964 12.2706L24 12.0312C24 7.34786 20.5829 4.03125 16 4.03125ZM16 14.9741C17.3807 14.9741 18.5 13.8548 18.5 12.4741C18.5 11.0934 17.3807 9.97406 16 9.97406C14.6193 9.97406 13.5 11.0934 13.5 12.4741C13.5 13.8548 14.6193 14.9741 16 14.9741Z" fill="#000000"></path></svg> <a class="FSs location-link-text">Detecting...</a> <svg width=16 height=16 viewBox="0 0 32 32" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M6.29289 11.2929C6.65338 10.9324 7.22061 10.9047 7.6129 11.2097L7.70711 11.2929L16 19.585L24.2929 11.2929C24.6534 10.9324 25.2206 10.9047 25.6129 11.2097L25.7071 11.2929C26.0676 11.6534 26.0953 12.2206 25.7903 12.6129L25.7071 12.7071L16.7071 21.7071C16.3466 22.0676 15.7794 22.0953 15.3871 21.7903L15.2929 21.7071L6.29289 12.7071C5.90237 12.3166 5.90237 11.6834 6.29289 11.2929Z" fill="#000000"></path></svg></div><div class=nav-links-container><a href="/my-account/my-quick-buy-again" class="menu-toggler buy-again-toggler nav-link FSs"><svg width=38 height=16 viewBox="0 0 38 16" fill=none xmlns="http://www.w3.org/2000/svg"><rect width=38 height=16 rx=4 fill="#AA0006"></rect><path d="M14.2939 3.89062V11H13.3467L9.76758 5.5166V11H8.8252V3.89062H9.76758L13.3613 9.38867V3.89062H14.2939ZM20.4805 10.2334V11H16.7158V10.2334H20.4805ZM16.9062 3.89062V11H15.9639V3.89062H16.9062ZM19.9824 6.94727V7.71387H16.7158V6.94727H19.9824ZM20.4316 3.89062V4.66211H16.7158V3.89062H20.4316ZM23.5176 8.85156L24.9287 3.89062H25.6123L25.2168 5.81934L23.6982 11H23.0195L23.5176 8.85156ZM22.0576 3.89062L23.1807 8.75391L23.5176 11H22.8438L21.1201 3.89062H22.0576ZM27.4385 8.74902L28.5371 3.89062H29.4795L27.7607 11H27.0869L27.4385 8.74902ZM25.7148 3.89062L27.0869 8.85156L27.585 11H26.9062L25.4414 5.81934L25.041 3.89062H25.7148Z" fill=white></path></svg><div class="btn-container__text nav-link" dir=auto>Buy Again</div></a><button class="FSs desktop-link-text deals-menu-toggler" type=button>Deals</button> <a href="/shop-by-room" class="FSs nav-link desktop-link-text">Shop By Room</a> <a href="/Interactive-Catalogue" class="FSs nav-link desktop-link-text">Catalogue</a> <a href="https://blog.builders.co.za" target=_blank class="FSs nav-link desktop-link-text">Blog</a> <a href="/builders-plus" class="FSs nav-link desktop-link-text">Builders+</a> <a href="/store-finder" class="FSs nav-link desktop-link-text">Store Locator</a> <a href="/contact-us" class="FSs nav-link desktop-link-text">Contact Us</a></div></div></div></div></header><header id=mobile-default-header class=mobile-header><div class=header-container><div class=logo-container><div class=left><div class=hamburger-mobile-icon><svg width=24 height=24 viewBox="0 0 24 24" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M21.75 3.75C22.1642 3.75 22.5 4.08579 22.5 4.5C22.5 4.8797 22.2178 5.19349 21.8518 5.24315L21.75 5.25H2.25C1.83579 5.25 1.5 4.91421 1.5 4.5C1.5 4.1203 1.78215 3.80651 2.14823 3.75685L2.25 3.75H21.75ZM21.75 18.75C22.1642 18.75 22.5 19.0858 22.5 19.5C22.5 19.8797 22.2178 20.1935 21.8518 20.2432L21.75 20.25H2.25C1.83579 20.25 1.5 19.9142 1.5 19.5C1.5 19.1203 1.78215 18.8065 2.14823 18.7568L2.25 18.75H21.75ZM22.5 12C22.5 11.5858 22.1642 11.25 21.75 11.25H2.25L2.14823 11.2568C1.78215 11.3065 1.5 11.6203 1.5 12C1.5 12.4142 1.83579 12.75 2.25 12.75H21.75L21.8518 12.7432C22.2178 12.6935 22.5 12.3797 22.5 12Z" fill="#222223"></path></svg></div><a href="/" class=logo data-testid=headerLogo><svg width=48 height=46 viewBox="0 0 70 67" fill=none xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_13095_21081)"><path d="M3 -2H1V0V64V66H3H67H69V64V0V-2H67H3Z" fill="#FFD600" stroke=white stroke-width=4></path><path d="M37.4247 27.207H40.9605V31.6323L51.0235 38.3177H45.7831L32.2837 29.7177L18.7707 38.3177H13.5303L32.2837 25.8387L37.4247 29.2684V27.207Z" fill=white></path><path d="M12.6046 42.0355C12.5983 41.9674 12.6056 41.8989 12.6261 41.8337C12.6467 41.7686 12.68 41.7082 12.7243 41.6561C12.7731 41.6133 12.83 41.5806 12.8917 41.5601C12.9533 41.5395 13.0185 41.5315 13.0832 41.5365C13.4061 41.5365 13.5687 41.7103 13.5687 42.0558V49.0708C13.5777 49.2137 13.5343 49.3549 13.4468 49.4682C13.3423 49.5459 13.2157 49.5878 13.0855 49.5878C12.9554 49.5878 12.8287 49.5459 12.7243 49.4682C12.6375 49.3546 12.595 49.2134 12.6046 49.0708V42.0355ZM12.6046 37.2037H9.82974L9.80942 37.215V51.1864H11.9182L12.1621 50.8003L12.6656 51.139C13.0225 51.2881 13.408 51.3567 13.7945 51.3399C14.6118 51.3399 15.262 51.1337 15.7452 50.7213C15.9349 50.5742 16.0893 50.3865 16.1972 50.1721C16.305 49.9576 16.3635 49.7217 16.3684 49.4817V41.3536C16.3686 41.1326 16.3159 40.9147 16.2145 40.7182C16.1132 40.5218 15.9662 40.3525 15.7858 40.2247C15.3717 39.9084 14.8591 39.7485 14.3386 39.7731C13.9875 39.7689 13.637 39.803 13.2932 39.8747C13.0454 39.9268 12.8133 40.0367 12.6159 40.1953L12.6046 37.2037ZM56.7494 46.6301H53.9564V49.0482C53.9564 49.8987 54.2846 50.5113 54.9409 50.8861C55.476 51.1931 56.2278 51.3376 57.1987 51.3376C58.1695 51.3376 58.9688 51.1638 59.531 50.8161C60.1858 50.4187 60.5131 49.7925 60.5131 48.9376V47.242C60.5288 46.9594 60.4853 46.6767 60.3854 46.4119C60.2855 46.1471 60.1313 45.9062 59.9329 45.7044C59.7462 45.5162 59.257 45.2152 58.4653 44.8013L57.3793 44.2233C57.1913 44.1141 57.0363 43.9562 56.9306 43.7662C56.8249 43.5763 56.7724 43.3613 56.7787 43.144V42.0851C56.7725 42.0093 56.7818 41.933 56.8058 41.8609C56.8299 41.7887 56.8683 41.7221 56.9187 41.6652C56.9631 41.6201 57.0163 41.5844 57.0749 41.5603C57.1334 41.5363 57.1963 41.5243 57.2596 41.5252C57.3218 41.5267 57.3828 41.5421 57.4383 41.5702C57.4938 41.5983 57.5423 41.6385 57.5802 41.6877C57.63 41.7407 57.6683 41.8032 57.6928 41.8716C57.7172 41.94 57.7274 42.0127 57.7225 42.0851V44.3023H60.4544V42.0648C60.4544 41.2136 60.1383 40.6017 59.5129 40.2292C58.9869 39.9221 58.2418 39.7776 57.2777 39.7776C56.3136 39.7776 55.5166 39.9515 54.9679 40.2969C54.3403 40.6988 54.0264 41.325 54.0264 42.1754V43.6949C53.9994 44.1345 54.1193 44.5706 54.3674 44.9345C54.7495 45.3299 55.1991 45.6541 55.695 45.8918C56.1465 46.1311 56.6116 46.3863 57.1219 46.6527C57.4832 46.8785 57.6615 47.3774 57.6615 48.1496V49.0279C57.6709 49.1835 57.6297 49.3379 57.5441 49.4682C57.5064 49.5169 57.4571 49.5554 57.4007 49.5802C57.3443 49.6051 57.2826 49.6154 57.2212 49.6104C57.1573 49.6143 57.0934 49.6035 57.0343 49.5788C56.9752 49.5541 56.9225 49.5163 56.8803 49.4682C56.7922 49.3389 56.7493 49.1841 56.7584 49.0279L56.7494 46.6301ZM49.9759 39.8567H47.1762V51.1841H49.9624V42.0761C49.9561 42.0083 49.9637 41.9399 49.9847 41.8751C50.0056 41.8103 50.0395 41.7504 50.0843 41.699C50.1335 41.6552 50.1911 41.6218 50.2536 41.6009C50.316 41.5799 50.3821 41.5718 50.4478 41.5771C50.7662 41.5771 50.9287 41.751 50.9287 42.0964V44.5552H53.7216V41.3942C53.721 41.1734 53.6678 40.9558 53.5665 40.7595C53.4653 40.5632 53.3188 40.3938 53.1391 40.2653C52.7319 39.9348 52.2182 39.7638 51.6941 39.7844C51.34 39.7799 50.987 39.827 50.6465 39.9244C50.4008 39.9839 50.1701 40.0938 49.9691 40.2473L49.9759 39.8567ZM42.498 42.0942C42.4919 42.0183 42.5011 41.9421 42.5251 41.8699C42.5492 41.7977 42.5876 41.7312 42.638 41.6742C42.7324 41.5826 42.8587 41.5314 42.9902 41.5314C43.1217 41.5314 43.2481 41.5826 43.3425 41.6742C43.4296 41.7961 43.4712 41.9447 43.4599 42.0942V44.7042H42.498V42.0942ZM39.7051 42.1732V48.9466C39.7051 49.8136 40.0257 50.4466 40.667 50.8454C41.2043 51.1796 41.969 51.3467 42.9609 51.3467C43.9498 51.3467 44.7152 51.1931 45.2481 50.8951C45.5717 50.7145 45.8379 50.4462 46.016 50.1211C46.1942 49.796 46.277 49.4273 46.255 49.0573V46.7498H43.4531V49.0302C43.4621 49.185 43.421 49.3386 43.3357 49.4682C43.2894 49.5179 43.2324 49.5565 43.1691 49.5811C43.1057 49.6057 43.0377 49.6158 42.9699 49.6104C42.9029 49.6151 42.8357 49.6047 42.7732 49.5801C42.7107 49.5555 42.6545 49.5173 42.6087 49.4682C42.5234 49.3386 42.4822 49.185 42.4913 49.0302V46.393H46.2483V42.0761C46.2483 41.2249 45.9096 40.613 45.2413 40.2405C44.6919 39.9394 43.9295 39.7889 42.9541 39.7889C41.9787 39.7889 41.2081 39.962 40.6421 40.3082C40.0129 40.7101 39.6983 41.3363 39.6983 42.1867L39.7051 42.1732ZM35.0111 42.0671C35.0111 41.7216 35.1692 41.5478 35.492 41.5478C35.5557 41.5446 35.6192 41.5555 35.6781 41.5797C35.7371 41.6039 35.7899 41.6408 35.833 41.6877C35.8818 41.7334 35.9198 41.7892 35.9444 41.8513C35.969 41.9134 35.9795 41.9801 35.9752 42.0467V49.0821C35.9832 49.2248 35.9399 49.3657 35.8533 49.4795C35.8039 49.5222 35.7466 49.5547 35.6846 49.5753C35.6226 49.5958 35.5572 49.6039 35.492 49.5991C35.4269 49.6043 35.3614 49.5964 35.2993 49.5758C35.2373 49.5553 35.18 49.5225 35.1308 49.4795C35.044 49.3659 35.0015 49.2247 35.0111 49.0821V42.0671ZM32.216 41.3694V49.4975C32.2205 49.7499 32.2825 49.998 32.3971 50.2229C32.5117 50.4478 32.676 50.6437 32.8775 50.7958C33.3291 51.1706 33.9725 51.3557 34.7876 51.3557C35.1792 51.3723 35.5698 51.3038 35.9323 51.1548C36.0999 51.0458 36.2613 50.9275 36.4155 50.8003L36.6548 51.1796H38.7681V37.2037H35.9752V40.1999C35.7605 40.0564 35.5208 39.9546 35.2685 39.8996C34.9341 39.8161 34.5904 39.7751 34.2457 39.7776C33.7188 39.7521 33.1996 39.9119 32.7782 40.2292C32.6025 40.3601 32.4601 40.5305 32.3625 40.7266C32.2648 40.9227 32.2146 41.139 32.216 41.3581V41.3694ZM31.288 37.2015H28.4928V51.1864H31.288V37.2015ZM27.5649 39.8567H24.7697V51.1864H27.5649V39.8567ZM27.5649 37.2037H24.7697V39.2358H27.5649V37.2037ZM20.0847 39.8589H17.2896V49.7662C17.2886 49.9852 17.3389 50.2014 17.4366 50.3974C17.5342 50.5935 17.6764 50.7639 17.8517 50.8951C18.2752 51.2084 18.793 51.3677 19.3193 51.3467C19.6744 51.3536 20.028 51.2994 20.3647 51.1864C20.615 51.1099 20.846 50.9805 21.042 50.8071V51.1864H23.8417V39.8589H21.0488V49.0889C21.0565 49.226 21.013 49.3612 20.9269 49.4682C20.8775 49.5109 20.8202 49.5434 20.7582 49.564C20.6962 49.5845 20.6308 49.5926 20.5656 49.5878C20.2428 49.5878 20.0847 49.414 20.0847 49.0708V39.8589ZM63.0577 52.6065H6.94425V39.1251L9.81393 37.2083V37.197H9.83425L32.3379 22.1712L35.273 24.122H43.8527V29.8478L53.5613 36.33H63.0577V52.6065ZM63.735 35.6729H53.7645L44.5075 29.5046V23.4582H35.4537L32.3243 21.3674L6.26465 38.7729V53.2839H63.735V35.6729Z" fill="#231F20"></path></g><rect x=1.5 y=-1.5 width=67 height=67 stroke=white stroke-width=3></rect><defs><clipPath id=clip0_13095_21081><rect x=3 width=64 height=64 fill=white></rect></clipPath></defs></svg></a></div><div class=right><a aria-label=Cart role=button href="/cart" class="btn-container menu-toggler cart__icon-wrapper"><svg width=24 height=24 viewBox="0 0 32 32" fill=none xmlns="http://www.w3.org/2000/svg"><path fill-rule=evenodd clip-rule=evenodd d="M7.99327 4.38338C7.93551 3.88604 7.51284 3.5 7 3.5H3L2.88338 3.50673C2.38604 3.56449 2 3.98716 2 4.5L2.00673 4.61662C2.06449 5.11396 2.48716 5.5 3 5.5H6V20.5L6.00673 20.6166C6.06449 21.114 6.48716 21.5 7 21.5H29L29.1166 21.4933C29.614 21.4355 30 21.0128 30 20.5V8.5L29.9933 8.38338C29.9355 7.88604 29.5128 7.5 29 7.5H8V4.5L7.99327 4.38338ZM8 9.5H28V19.5H8V9.5ZM25.818 25C25.818 26.3807 24.6987 27.5 23.318 27.5C21.9373 27.5 20.818 26.3807 20.818 25C20.818 23.6193 21.9373 22.5 23.318 22.5C24.6987 22.5 25.818 23.6193 25.818 25ZM11.318 27.5C12.6987 27.5 13.818 26.3807 13.818 25C13.818 23.6193 12.6987 22.5 11.318 22.5C9.93728 22.5 8.81799 23.6193 8.81799 25C8.81799 26.3807 9.93728 27.5 11.318 27.5Z" fill=black></path></svg></a></div></div><div class=search-bar-container><input placeholder="What can we help you find?" maxlength=100 autocapitalize=sentences autocomplete=on autocorrect=on dir=auto enterkeyhint=search spellcheck=true class=search-input-bar data-testid=searchInputField value=""/><div class=search-btn-container><div aria-disabled=true aria-label=Search role=button tabindex=-1 class=""><svg width=24 height=24 viewBox="0 0 32 32" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M14 5a9 9 0 017.032 14.617l5.1 5.1a.5.5 0 010 .708l-.707.707a.5.5 0 01-.707 0l-5.1-5.1A9 9 0 1114 5zm0 2a7 7 0 100 14 7 7 0 000-14z" fill="#FFFFFF"></path></svg></div></div></div><div class=mobile-location-container><svg width=16 height=16 viewBox="0 0 32 32" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M16 2.03125C21.5228 2.03125 26 6.08268 26 12.0312C26 16.6949 22.6667 22.6758 16 29.9741C9.33333 22.6724 6 16.6915 6 12.0312C6 6.07829 10.4772 2.03125 16 2.03125ZM16 4.03125C11.4154 4.03125 8 7.34513 8 12.0312C8 15.6712 10.5359 20.5782 15.6998 26.6166L16 26.9653L16.3004 26.6171C21.352 20.7125 23.8885 15.8882 23.9964 12.2706L24 12.0312C24 7.34786 20.5829 4.03125 16 4.03125ZM16 14.9741C17.3807 14.9741 18.5 13.8548 18.5 12.4741C18.5 11.0934 17.3807 9.97406 16 9.97406C14.6193 9.97406 13.5 11.0934 13.5 12.4741C13.5 13.8548 14.6193 14.9741 16 14.9741Z" fill="#000000"></path></svg><p class="FSs mobile-deliver-text">Detecting...</p><svg width=16 height=16 viewBox="0 0 32 32" fill=none><path fill-rule=evenodd clip-rule=evenodd d="M6.29289 11.2929C6.65338 10.9324 7.22061 10.9047 7.6129 11.2097L7.70711 11.2929L16 19.585L24.2929 11.2929C24.6534 10.9324 25.2206 10.9047 25.6129 11.2097L25.7071 11.2929C26.0676 11.6534 26.0953 12.2206 25.7903 12.6129L25.7071 12.7071L16.7071 21.7071C16.3466 22.0676 15.7794 22.0953 15.3871 21.7903L15.2929 21.7071L6.29289 12.7071C5.90237 12.3166 5.90237 11.6834 6.29289 11.2929Z" fill="#000000"></path></svg></div></div></header><div id=react-app><div id=loader-wrapper style="width:100%;display:flex;flex:1 1 0"><div id=ctn><div id=loader><svg height="100%" viewBox="0 0 32 32" width="100%"><circle cx=16 cy=16 fill=none r=14 stroke-width=4 style="stroke:rgb(34,34,35);opacity:.2"></circle><circle cx=16 cy=16 fill=none r=14 stroke-width=4 style="stroke:rgb(34,34,35);stroke-dasharray:80;stroke-dashoffset:60"></circle></svg></div><span id=loader-text>Loading...</span></div></div></div><script defer=defer src="/runtimechunk~main.dec3ab75e20e1b2d649e.js"></script><script defer=defer src="/vendor_react.921720b8e3a8f4641099.js"></script><script defer=defer src="/vendor-cdd60c62.555d2f6410cd18396b4c.js"></script><script defer=defer src="/vendor-229eafb5.0ae129734648e15b698b.js"></script><script defer=defer src="/main.3264e916f7e578c5463a.js"></script><script defer=defer>function onStartup(){try{var e="true"===(u=new RegExp(`${"BL_PPD"}=([^;]+)`).exec(document.cookie),(u?.length?decodeURI(u[1]):"").toLowerCase()),t=JSON.parse(localStorage.getItem("BL_HEADER_INFO")),o=t&&t.isLoggedIn;if(o&&(document.querySelector(".sign-in-text").textContent="Hi, "+t.name,document.querySelector(".buy-again-toggler").style.opacity=1),!e&&"/"===document.location.pathname&&!o){var a=atob(window.__ZBE__.uh)||"",n=window.innerWidth>1024,r=JSON.parse(localStorage.getItem("BL_ZONE_CODE"))||"B14",c=n?"web":"msite",i=document.createElement("link");i.setAttribute("rel","preload"),i.setAttribute("href",a+"/web/v2/builders/channel/"+c+"/zone/"+r+"/users/anonymous/cms/pages?pageLabelOrId=homepageocc&disableProductData=true"),i.setAttribute("as","fetch"),i.setAttribute("crossorigin","anonymous"),document.head.appendChild(i)}}catch(e){}var u}onStartup()</script><script defer=defer src="https://accounts.google.com/gsi/client"></script><script defer=defer src="https://apps.bazaarvoice.com/deployments/builders/main_site/production/en_ZA/bv.js"></script><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PCPNHSJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript></body></html>
```

### `project_status_snapshot.md`
**📦 Universal Recycling Orders Project Snapshot**
```python
# 📦 Universal Recycling Orders Project Snapshot

📁 Analyzing file: backend/endpoints/orders.py

## 🧠 Backend Routes
- POST /orders → ✅ Found: line 40: @router.post("")
- POST /orders/receive → ❌ Not found
- GET /orders/print_to_file → ❌ Not found
- GET /orders/print → ❌ Not found
- GET /orders/pending → ❌ Not found
- GET /orders/audit → ❌ Not found
- POST /orders/upload_attachment → ❌ Not found

## 🎨 Frontend Templates

- index.html → ❌ Empty
- pending.html → ❌ Empty
- print_template.html → ✅ Populated
- received.html → ❌ Empty
- maintenance.html → ❌ Empty
- audit.html → ❌ Empty
- new_order.html → ❌ Empty

## ⚙️ Scripts Detected

- fix_escaped_triple_quotes.py
- fix_print_order_items.py
- generate_project_status_snapshot.py
- inject_filter_route.py
- insert_audit_route.py
- insert_audit_tracking_into_receive.py
- insert_awaiting_auth_order.py
- insert_extended_order_route.py
- insert_get_all_orders.py
- insert_next_order_number_route.py
- insert_pending_route.py
- insert_print_route.py
- insert_print_to_file_route.py
- insert_receive_route.py
- insert_test_order.py
- insert_twilio_placeholder.py
- insert_upload_attachment.py
- patch_ordercreate_model.py
- prepare_lookup_tables.py
- start_server_background.py

## 🧪 Test Scripts

- test_create_full_order.py
- test_pipeline_end_to_end.py
- test_receive_po_test_001.py

## 📋 Lookup Table Check

- suppliers: ✅ Populated (3 rows)
- projects: ❌ Empty (0 rows)
- items: ❌ Empty (0 rows)
- requesters: ❌ Table not found

## 🗃️ Database File

- ✅ Found at data/orders.db

## ✅ Summary

- You can upload this file to a new ChatGPT session to instantly re-brief Cathy.
- File generated automatically. No need to manually track dev state.

```

### `frontend/.DS_Store`
**(No description)**
```python
<!-- ERROR reading .DS_Store: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte -->
```

### `frontend/static/.DS_Store`
**(No description)**
```python
<!-- ERROR reading .DS_Store: 'utf-8' codec can't decode byte 0xff in position 1072: invalid start byte -->
```

### `frontend/static/css/style.css`
**(No description)**
```python
mkdir -p frontend/static/js frontend/static/css && \
cat <<EOF > frontend/static/css/style.css
body {
  font-family: Arial, sans-serif;
  margin: 2rem;
}
h2 {
  margin-bottom: 1rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
}
.actions {
  margin-top: 1.5rem;
}
label.inline {
  margin-right: 2rem;
}
EOF

cat <<EOF > frontend/static/js/date_utils.js
export function setDateInputFormat(inputId) {
  const display = document.getElementById(\`\${inputId}-display\`);
  const hidden = document.getElementById(inputId);

  if (!display || !hidden) return;

  display.addEventListener("click", () => hidden.showPicker());
  hidden.addEventListener("input", () => {
    const [year, month, day] = hidden.value.split("-");
    display.value = \`\${day}/\${month}/\${year}\`;
  });
}
EOF


```

### `frontend/static/js/new_order.js`
**(No description)**
```python
let itemsList = [];
let projectsList = [];

function updateGrandTotal() {
  let sum = 0;
  document.querySelectorAll(".line-total").forEach(cell => {
    sum += parseFloat(cell.textContent) || 0;
  });
  document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

function updateTotal(input) {
  const row = input.closest("tr");
  const qty = parseFloat(row.cells[3].querySelector("input").value) || 0;
  const price = parseFloat(row.cells[4].querySelector("input").value) || 0;
  row.cells[5].textContent = (qty * price).toFixed(2);
  updateGrandTotal();
}

function autoFillDescription(sel) {
  const desc = sel.selectedOptions[0]?.dataset.description ?? "";
  sel.closest("tr").querySelector("td:nth-child(2) input").value = desc;
}

function deleteRow(btn) {
  btn.closest("tr").remove();
  updateGrandTotal();
}

function addRow() {
  const tbody = document.getElementById("items-body");
  const row = tbody.insertRow();

  const itemOpts = itemsList.map(i =>
    `<option value="${i.item_code}" data-description="${i.item_description}">${i.item_code} — ${i.item_description}</option>`
  ).join("");

  const projOpts = projectsList.map(p =>
    `<option value="${p.project_code}">${p.project_code} — ${p.project_name}</option>`
  ).join("");

  row.innerHTML = `
    <td>
      <select onchange="autoFillDescription(this)">
        <option value="">Select</option>
        ${itemOpts}
      </select>
    </td>
    <td><input type="text" placeholder="Description"></td>
    <td>
      <select>
        <option value="">Select</option>
        ${projOpts}
      </select>
    </td>
    <td><input type="number" value="1" min="1" onchange="updateTotal(this)"></td>
    <td><input type="number" value="0" min="0" onchange="updateTotal(this)"></td>
    <td class="line-total">0.00</td>
    <td><button type="button" onclick="deleteRow(this)">❌</button></td>
  `;
  updateGrandTotal();
}

async function loadDropdowns() {
  try {
    const [supR, reqR, itmR, prjR, numR] = await Promise.all([
      fetch("/lookups/suppliers").then(r => r.json()),
      fetch("/lookups/requesters").then(r => r.json()),
      fetch("/lookups/items").then(r => r.json()),
      fetch("/lookups/projects").then(r => r.json()),
      fetch("/orders/next_order_number").then(r => r.json())
    ]);

    const supplierDropdown = document.getElementById("supplier");
    supplierDropdown.innerHTML = '<option value="">Select supplier</option>';
    supR.suppliers.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s.id;
      opt.textContent = `${s.account_number} — ${s.name}`;
      supplierDropdown.appendChild(opt);
    });

    const requesterDropdown = document.getElementById("requester");
    requesterDropdown.innerHTML = '<option value="">Select requester</option>';
    reqR.requesters.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r.id;
      opt.textContent = r.name;
      requesterDropdown.appendChild(opt);
    });

    itemsList = itmR.items || [];
    projectsList = prjR.projects || [];

    document.getElementById("order-number").value = numR.next_order_number || "ORD-????";
    document.getElementById("request-date").valueAsDate = new Date();

    addRow();
  } catch (err) {
    console.error("Lookup loading failed", err);
    alert("⚠️ Failed to load dropdowns. Check server or database.");
  }
}

function previewOrder() {
  const rd = document.getElementById("request-date").value;
  const rq = document.getElementById("requester").value;
  const sp = document.getElementById("supplier").value;
  const nt = document.querySelector("textarea[name='note_to_supplier']").value;

  const items = Array.from(document.querySelectorAll("#items-body tr"))
    .map(row => {
      const c = row.querySelectorAll("td");
      return {
        item_code: c[0].querySelector("select").value,
        item_description: c[1].querySelector("input").value,
        project: c[2].querySelector("select").value,
        qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
        price: parseFloat(c[4].querySelector("input").value) || 0
      };
    })
    .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

  alert("Preview:\n" + JSON.stringify({ request_date: rd, requester_id: rq, supplier_id: sp, note_to_supplier: nt, items }, null, 2));
}

async function submitOrder() {
  const rd = document.getElementById("request-date").value;
  const rqId = document.getElementById("requester").value;
  const spId = document.getElementById("supplier").value;
  const nt = document.querySelector("textarea[name='note_to_supplier']").value;
  const rows = document.querySelectorAll("#items-body tr");

  const items = Array.from(rows)
    .map(row => {
      const c = row.querySelectorAll("td");
      return {
        item_code: c[0].querySelector("select").value,
        item_description: c[1].querySelector("input").value,
        project: c[2].querySelector("select").value,
        qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
        price: parseFloat(c[4].querySelector("input").value) || 0
      };
    })
    .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

  if (!rd || !rqId || !spId || items.length === 0) {
    return alert("⚠️ Fill date, requester, supplier & at least one complete line.");
  }

  try {
    const res = await fetch("/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        request_date: rd,
        requester_id: rqId,
        supplier_id: spId,
        note_to_supplier: nt,
        items
      })
    });

    const data = await res.json();

    if (res.ok && data.message === "Order created successfully") {
      const orderNumber = data.order?.order_number || document.getElementById("order-number").value;
      alert(`✅ Order ${orderNumber} created.`);
      location.reload();
    } else {
      const detail = data.detail || data.message || "Unknown error.";
      alert(`❌ ${detail}`);
    }
  } catch (err) {
    console.error("Submit failed", err);
    alert("❌ Submission failed.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadDropdowns();
  document.getElementById("add-line").addEventListener("click", addRow);
  document.getElementById("preview-order").addEventListener("click", previewOrder);
  document.getElementById("submit-order").addEventListener("click", submitOrder);
});

```

### `frontend/static/js/pending_orders.js`
**(No description)**
```python
import { setDateInputFormat } from "/static/js/date_utils.js";

function populateDropdown(selectId, items, labelFunc) {
  const dropdown = document.getElementById(selectId);
  dropdown.innerHTML = `<option value="">All</option>`;
  items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = item.id;
    opt.textContent = labelFunc(item);
    dropdown.appendChild(opt);
  });
}

function populateTable(data) {
  const tbody = document.getElementById("pending-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No pending orders found.";
    return;
  }

  data.orders.forEach(order => {
    const row = tbody.insertRow();
    row.innerHTML = `
      <td>${order.request_date}</td>
      <td>${order.order_number}</td>
      <td>${order.requester}</td>
      <td>${order.supplier}</td>
      <td>R${order.total_value.toFixed(2)}</td>
      <td>${order.status}</td>
      <td><button onclick="alert('Expand feature coming soon')">⬇️</button></td>
    `;
  });
}

async function loadFiltersAndOrders() {
  try {
    const [suppliersRes, requestersRes] = await Promise.all([
      fetch("/lookups/suppliers").then(res => res.json()),
      fetch("/lookups/requesters").then(res => res.json())
    ]);

    populateDropdown("filter-supplier", suppliersRes.suppliers, s => `${s.account_number} — ${s.name}`);
    populateDropdown("filter-requester", requestersRes.requesters, r => r.name);

    runFilters();
  } catch (err) {
    console.error("Failed to load filters", err);
  }
}

async function runFilters() {
  const supplierId = document.getElementById("filter-supplier").value;
  const requesterId = document.getElementById("filter-requester").value;
  const status = document.getElementById("filter-status").value;
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;

  const params = new URLSearchParams();
  if (supplierId) params.append("supplier_id", supplierId);
  if (requesterId) params.append("requester_id", requesterId);
  if (status) params.append("status", status);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/pending?${params.toString()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch filtered orders", err);
  }
}

function clearFilters() {
  document.getElementById("filter-supplier").value = "";
  document.getElementById("filter-requester").value = "";
  document.getElementById("filter-status").value = "";
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  runFilters();
}

document.addEventListener("DOMContentLoaded", () => {
  setDateInputFormat("start-date");
  setDateInputFormat("end-date");
  loadFiltersAndOrders();

  document.getElementById("run-filters").addEventListener("click", runFilters);
  document.getElementById("clear-filters").addEventListener("click", clearFilters);
});


```

### `frontend/static/js/shared_filters.js`
**(No description)**
```python
// Load requesters into a given select element
export async function loadRequesters(selectId) {
    try {
      const res = await fetch("/lookups/requesters");
      const data = await res.json();
      const select = document.getElementById(selectId);
      if (!select) return;
  
      select.innerHTML = '<option value="All">All</option>';
      data.requesters.forEach(r => {
        const opt = document.createElement("option");
        opt.value = r.name;
        opt.textContent = r.name;
        select.appendChild(opt);
      });
    } catch (err) {
      console.error(`❌ Failed to load requesters for ${selectId}:`, err);
    }
  }
  
  // Load suppliers into a given select element
  export async function loadSuppliers(selectId) {
    try {
      const res = await fetch("/lookups/suppliers");
      const data = await res.json();
      const select = document.getElementById(selectId);
      if (!select) return;
  
      select.innerHTML = '<option value="All">All</option>';
      data.suppliers.forEach(s => {
        const opt = document.createElement("option");
        opt.value = s.name;
        opt.textContent = s.name;
        select.appendChild(opt);
      });
    } catch (err) {
      console.error(`❌ Failed to load suppliers for ${selectId}:`, err);
    }
  }
  
```

### `frontend/static/js/components/date_input.js`
**(No description)**
```python
export function attachSmartDateInput(id) {
  const input = document.getElementById(id);
  if (!input) return;

  input.setAttribute("type", "text");
  input.setAttribute("placeholder", "dd/mm/yyyy");
  input.setAttribute("maxlength", "10");
  input.setAttribute("inputmode", "numeric");
  input.style.fontFamily = "monospace";

  input.addEventListener("input", () => {
    const cursorPos = input.selectionStart;
    let value = input.value.replace(/\D/g, "").slice(0, 8);
    let formatted = "";

    if (value.length > 2) {
      formatted += value.substr(0, 2) + "/";
      if (value.length > 4) {
        formatted += value.substr(2, 2) + "/";
        formatted += value.substr(4, 4);
      } else {
        formatted += value.substr(2);
      }
    } else {
      formatted = value;
    }

    input.value = formatted;

    // Adjust and restore cursor position
    const slashesBefore = (formatted.slice(0, cursorPos).match(/\//g) || []).length;
    const rawCursorPos = cursorPos - slashesBefore;
    let newCursorPos = rawCursorPos;

    if (rawCursorPos > 1) newCursorPos += 1;
    if (rawCursorPos > 3) newCursorPos += 1;
    input.setSelectionRange(newCursorPos, newCursorPos);
  });

  input.addEventListener("keydown", (e) => {
    const pos = input.selectionStart;
    const val = input.value;

    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      e.preventDefault();
      let newPos = pos;

      if (e.key === "ArrowRight") {
        newPos = pos === 2 || pos === 5 ? pos + 2 : pos + 1;
      } else {
        newPos = pos === 3 || pos === 6 ? pos - 2 : pos - 1;
      }

      newPos = Math.max(0, Math.min(newPos, val.length));
      input.setSelectionRange(newPos, newPos);
    }

    const allowed = [
      "Backspace", "Tab", "ArrowLeft", "ArrowRight", "Delete", "Home", "End", "Enter"
    ];
    if (!/^\d$/.test(e.key) && !allowed.includes(e.key)) {
      e.preventDefault();
    }
  });
}

```

### `frontend/templates/audit.html`
**(No description)**
```python

```

### `frontend/templates/home.html`
**(No description)**
```python
<!-- frontend/templates/home.html -->
<html>
  <body>
    <h2>Welcome, {{ username }}</h2>
    <p><a href="/logout">Logout</a></p>
  </body>
</html>


```

### `frontend/templates/index.html`
**(No description)**
```python

```

### `frontend/templates/login.html`
**(No description)**
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login - Universal Recycling</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f3f3;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 0 12px rgba(0,0,0,0.1);
            width: 300px;
        }
        h2 {
            margin-bottom: 1rem;
            text-align: center;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.6rem;
            margin: 0.5rem 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 0.6rem;
            background: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form method="post" action="/login">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>

```

### `frontend/templates/maintenance.html`
**(No description)**
```python

```

### `frontend/templates/new_order.html`
**(No description)**
```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>New Order - Universal Recycling</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
    input, select, textarea, button { padding: 0.4rem; font-size: 1rem; }
    .inline { margin-right: 2rem; }
    button { cursor: pointer; }
  </style>
</head>
<body>
  <h2>Submit a New Order</h2>

  <div>
    <label class="inline">Request Date:
      <input type="date" id="request-date">
    </label>
    <label class="inline">Order Number:
      <input type="text" id="order-number" value="ORD-????" readonly>
    </label>
  </div><br>

  <div>
    <label class="inline">Requester:
      <select id="requester" name="requester_id">
        <option value="">Select requester</option>
      </select>
    </label>
    <label class="inline">Supplier:
      <select id="supplier" name="supplier_id">
        <option value="">Select supplier</option>
      </select>
    </label>
  </div><br>

  <label>Special Instructions for Supplier:</label><br>
  <textarea rows="3" cols="60" name="note_to_supplier"></textarea><br><br>

  <table>
    <thead>
      <tr>
        <th>Stock Code</th>
        <th>Description</th>
        <th>Project</th>
        <th>Qty</th>
        <th>Price</th>
        <th>Total</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody id="items-body"></tbody>
  </table>

  <button type="button" id="add-line">➕ Add New Line</button>

  <div class="actions">
    <h3>Total Order Value: <span id="grand-total">R0.00</span></h3>
    <button type="button" id="preview-order">Preview Order</button>
    <button type="button" id="submit-order">Submit</button>
  </div>

  <!-- ✅ Load external JavaScript for order logic -->
  <script src="/static/js/new_order.js"></script>
</body>
</html>

```

### `frontend/templates/pending_orders.html`
**(No description)**
```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Pending Orders</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: center; }
    .status { font-weight: bold; }
    .filters { margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
    .filters label { font-weight: bold; }
    input[type="text"], select {
      padding: 0.4rem;
      font-size: 1rem;
      font-family: monospace;
    }
    button {
      padding: 0.5rem 1rem;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <h2>Pending Orders</h2>

  <div class="filters">
    <label for="start-date">Start Date:</label>
    <input type="text" id="start-date" placeholder="dd/mm/yyyy" maxlength="10" />

    <label for="end-date">End Date:</label>
    <input type="text" id="end-date" placeholder="dd/mm/yyyy" maxlength="10" />

    <label for="filter-requester">Requester:</label>
    <select id="filter-requester"></select>

    <label for="filter-supplier">Supplier:</label>
    <select id="filter-supplier"></select>

    <button id="run-btn">Run</button>
    <button id="clear-btn">Clear</button>
  </div>

  <table>
    <thead>
      <tr>
        <th>Request Date</th>
        <th>Order Number</th>
        <th>Requester</th>
        <th>Supplier</th>
        <th>Total</th>
        <th>Status</th>
        <th>Actions (coming soon)</th>
      </tr>
    </thead>
    <tbody id="orders-body">
      <!-- Rows go here -->
    </tbody>
  </table>

  <script type="module">
    import { loadRequesters, loadSuppliers } from "/static/js/shared_filters.js";
    import { attachSmartDateInput } from "/static/js/components/date_input.js";

    async function loadPendingOrders(filters = {}) {
      try {
        const params = new URLSearchParams(filters).toString();
        const res = await fetch(`/orders/pending_data${params ? '?' + params : ''}`);
        const data = await res.json();
        const tbody = document.getElementById("orders-body");
        tbody.innerHTML = "";

        (data.orders || []).forEach(order => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${order.created_date || "?"}</td>
            <td>${order.order_number}</td>
            <td>${order.requester}</td>
            <td>${order.supplier || "—"}</td>
            <td>R${(order.total || 0).toFixed(2)}</td>
            <td class="status">${order.status}</td>
            <td>🔧</td>
          `;
          tbody.appendChild(row);
        });
      } catch (err) {
        alert("❌ Failed to load pending orders");
        console.error(err);
      }
    }

    function applyFilters() {
      const startDate = document.getElementById("start-date").value.trim();
      const endDate = document.getElementById("end-date").value.trim();
      const requester = document.getElementById("filter-requester").value;
      const supplier = document.getElementById("filter-supplier").value;

      const filters = {};
      if (startDate) filters.start_date = startDate;
      if (endDate) filters.end_date = endDate;
      if (requester && requester !== "All") filters.requester = requester;
      if (supplier && supplier !== "All") filters.supplier = supplier;

      loadPendingOrders(filters);
    }

    function clearFilters() {
      document.getElementById("start-date").value = "";
      document.getElementById("end-date").value = "";
      document.getElementById("filter-requester").value = "All";
      document.getElementById("filter-supplier").value = "All";
      loadPendingOrders();
    }

    document.addEventListener("DOMContentLoaded", () => {
      attachSmartDateInput("start-date");
      attachSmartDateInput("end-date");

      loadRequesters("filter-requester");
      loadSuppliers("filter-supplier");

      document.getElementById("run-btn").addEventListener("click", applyFilters);
      document.getElementById("clear-btn").addEventListener("click", clearFilters);

      loadPendingOrders();
    });
  </script>
</body>
</html>

```

### `frontend/templates/print_template.html`
**(No description)**
```python
<!DOCTYPE html>
<html>
<head>
    <title>Printable Order - {{ order.order_number }}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Order {{ order.order_number }}</h1>
    <p><strong>Status:</strong> {{ order.status }}</p>
    <p><strong>Created Date:</strong> {{ order.created_date }}</p>
    <p><strong>Received Date:</strong> {{ order.received_date or "N/A" }}</p>
    <p><strong>Total:</strong> {{ order.total }}</p>
    <p><strong>Requester:</strong> {{ order.requester }}</p>
    <p><strong>Order Note:</strong> {{ order.order_note or "None" }}</p>
    <p><strong>Supplier Note:</strong> {{ order.supplier_note or "None" }}</p>

    <h2>Line Items</h2>
    <table border="1" cellpadding="6" cellspacing="0">
        <thead>
            <tr>
                <th>Item Code</th>
                <th>Description</th>
                <th>Project</th>
                <th>Qty Ordered</th>
                <th>Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.item_code }}</td>
                <td>{{ item.item_description }}</td>
                <td>{{ item.project }}</td>
                <td>{{ item.qty_ordered }}</td>
                <td>{{ item.price }}</td>
                <td>{{ item.total }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>

```

### `frontend/templates/received.html`
**(No description)**
```python

```

### `backend/.DS_Store`
**(No description)**
```python
<!-- ERROR reading .DS_Store: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte -->
```

### `backend/__init__.py`
**(No description)**
```python
 
```

### `backend/database.py`
**Create tables and seed default settings.**
```python
import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

DB_PATH = "data/orders.db"
LOG_PATH = Path("logs/db_activity_log.txt")

def log_db_event(action: str, payload: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {action}: {json.dumps(payload, ensure_ascii=False)}\n")

def init_db() -> None:
    """Create tables and seed default settings."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requesters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT,
                    name TEXT,
                    telephone TEXT,
                    vat_number TEXT,
                    registration_number TEXT,
                    email TEXT,
                    contact_name TEXT,
                    contact_telephone TEXT,
                    address_line1 TEXT,
                    address_line2 TEXT,
                    address_line3 TEXT,
                    postal_code TEXT
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_number TEXT,
                    status TEXT,
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    received_date TEXT,
                    total REAL,
                    order_note TEXT,
                    note_to_supplier TEXT,
                    supplier_id INTEGER REFERENCES suppliers(id),
                    requester_id INTEGER REFERENCES requesters(id)
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    item_code TEXT,
                    item_description TEXT,
                    project TEXT,
                    qty_ordered REAL,
                    price REAL,
                    total REAL
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    upload_date TEXT NOT NULL
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER REFERENCES orders(id),
                    action TEXT,
                    details TEXT,
                    action_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER
                )""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )""")

            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('auth_threshold', '10000')"
            )
            cursor.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('order_number_start', 'PO001')"
            )

            conn.commit()
            log_db_event("init_db", {"status": "success"})
    except Exception as e:
        log_db_event("init_db_error", {"error": str(e)})
        raise


def create_order(order_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO orders (
                    order_number, status, created_date, total,
                    order_note, note_to_supplier, supplier_id, requester_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data["order_number"],
                order_data["status"],
                datetime.now().isoformat(),
                order_data["total"],
                order_data.get("order_note"),
                order_data.get("note_to_supplier"),
                order_data.get("supplier_id"),
                order_data["requester_id"]
            ))
            order_id = cursor.lastrowid

            for item in items:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, item_code, item_description, project,
                        qty_ordered, price, total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    item["item_code"],
                    item["item_description"],
                    item["project"],
                    item["qty_ordered"],
                    item["price"],
                    item["qty_ordered"] * item["price"]
                ))

            conn.commit()

            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]

            log_db_event("create_order", {
                "order_number": order_data["order_number"],
                "requester_id": order_data["requester_id"],
                "total": order_data["total"],
                "items_count": len(items)
            })

            return dict(zip(columns, row))
    except Exception as e:
        log_db_event("create_order_error", {"error": str(e)})
        raise


def get_setting(key: str) -> Optional[str]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            log_db_event("get_setting", {"key": key, "result": row[0] if row else None})
            return row[0] if row else None
    except Exception as e:
        log_db_event("get_setting_error", {"key": key, "error": str(e)})
        raise


def update_setting(key: str, value: str) -> None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """, (key, value))
            conn.commit()
            log_db_event("update_setting", {"key": key, "value": value})
    except Exception as e:
        log_db_event("update_setting_error", {"key": key, "error": str(e)})
        raise

```

### `backend/main.py`
**✅ Add the enhanced validation handler**
```python
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup, supplier_lookup_takealot
from backend.database import init_db
from pathlib import Path
import logging

# ✅ Add the enhanced validation handler
from scripts.add_debug_validation_handler import install_validation_handler

# Ensure log directory exists
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/server_startup.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Initialize DB
try:
    init_db()
    logging.info("✅ Database initialized successfully.")
except Exception as e:
    logging.exception("❌ Failed to initialize database")
    raise

app = FastAPI(
    title="Universal Recycling Purchase Order System",
    description="Purchase Order management system for Universal Recycling"
)

# ✅ Install the validation handler before anything else
install_validation_handler(app)

# Static Files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Limit in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")  # Replace in prod

# ✅ Routers
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(lookups.router)
app.include_router(ui_pages.router)
app.include_router(supplier_lookup.router)
app.include_router(supplier_lookup_takealot.router)

# Run
if __name__ == "__main__":
    import uvicorn
    try:
        logging.info("🚀 Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8004)
    except Exception as e:
        logging.exception("❌ Server failed to start")
        raise

```

### `backend/endpoints/__init__.py`
**API endpoints for Universal Recycling Purchase Order System**
```python
"""
API endpoints for Universal Recycling Purchase Order System
""" 
```

### `backend/endpoints/auth.py`
**backend/auth.py**
```python
# backend/auth.py

from fastapi import APIRouter, Request, Form, Response, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
DB_PATH = "data/orders.db"


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash, rights FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user_id, pw_hash, rights = user

        # Dummy check: skip real password checking for now
        # Replace this with hashed check later
        if password != "password":
            raise HTTPException(status_code=401, detail="Incorrect password")

        request.session["user_id"] = user_id
        request.session["username"] = username
        request.session["rights"] = rights

        return RedirectResponse(url="/", status_code=302)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {e}")


@router.get("/logout")
def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@router.get("/")
def home(request: Request):
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("home.html", {"request": request, "username": username})


```

### `backend/endpoints/lookups.py`
**(No description)**
```python
from fastapi import APIRouter, HTTPException
import sqlite3
from pathlib import Path
from datetime import datetime
import json

router = APIRouter(prefix="/lookups")

def log_lookup(endpoint: str, outcome: str, detail: str = ""):
    log_path = Path("logs/lookups_log.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        entry = {"time": timestamp, "endpoint": endpoint, "status": outcome}
        if detail:
            entry["detail"] = detail
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

@router.get("/suppliers")
def get_suppliers():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, account_number, name FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
        log_lookup("/suppliers", "success")
        return {"suppliers": suppliers}
    except Exception as e:
        log_lookup("/suppliers", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load suppliers: {e}")

@router.get("/requesters")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
        log_lookup("/requesters", "success")
        return {"requesters": requesters}
    except Exception as e:
        log_lookup("/requesters", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load requesters: {e}")

@router.get("/items")
def get_items():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT item_code, item_description FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
        log_lookup("/items", "success")
        return {"items": items}
    except Exception as e:
        log_lookup("/items", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load items: {e}")

@router.get("/projects")
def get_projects():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT project_code, project_name FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
        log_lookup("/projects", "success")
        return {"projects": projects}
    except Exception as e:
        log_lookup("/projects", "error", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to load projects: {e}")

```

### `backend/endpoints/orders.py`
**UPDATE order_items**
```python
from fastapi import APIRouter, HTTPException, Request, UploadFile, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import json
import shutil

from ..database import create_order, get_setting, update_setting
from ..utils.order_utils import generate_order_number, determine_status, validate_order_items

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="frontend/templates")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

@router.get("/next_order_number")
def get_next_order_number():
    try:
        current_number = get_setting("order_number_start")
        next_number = generate_order_number(current_number)
        return {"next_order_number": next_number}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "next_order_number"})
        raise HTTPException(status_code=500, detail=f"Failed to get next order number: {e}")

class OrderItem(BaseModel):
    item_code: str = Field(min_length=1)
    item_description: str = Field(min_length=1)
    project: str = Field(min_length=1)
    qty_ordered: float = Field(gt=0)
    price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.qty_ordered * self.price

class OrderCreate(BaseModel):
    order_number: Optional[str] = None
    requester_id: int = Field(gt=0)
    order_note: Optional[str] = None
    note_to_supplier: Optional[str] = None
    supplier_id: Optional[int] = None
    items: List[OrderItem] = Field(min_length=1)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

@router.post("")
async def create_new_order(order: OrderCreate):
    try:
        validate_order_items(order.items)
        total = order.total

        auth_threshold = float(get_setting("auth_threshold"))
        current_order_number = get_setting("order_number_start")

        if not order.order_number:
            order.order_number = generate_order_number(current_order_number)
            next_order_number = generate_order_number(order.order_number)
            update_setting("order_number_start", next_order_number)

        status = determine_status(total, auth_threshold)

        if total > auth_threshold:
            print(f"[WHATSAPP] Order {order.order_number} exceeds threshold, notify for auth.")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Invalid requester_id")

        order_data = order.model_dump()
        order_data["status"] = status
        order_data["total"] = total

        log_event("new_orders_log.txt", {"action": "submit_attempt", "order_data": order_data})

        result = create_order(order_data=order_data, items=[item.model_dump() for item in order.items])
        result["created_date"] = datetime.fromisoformat(result["created_date"]).strftime("%d/%m/%Y")

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM requesters WHERE id = ?", (order.requester_id,))
            name_row = cursor.fetchone()
            result["requester"] = name_row[0] if name_row else "Unknown"

        log_event("new_orders_log.txt", {"action": "submit_success", "order_number": order.order_number, "status": status})

        return {"message": "Order created successfully", "order": result}
    except sqlite3.Error as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite"})
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "value"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "unexpected"})
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

class ItemReceive(BaseModel):
    order_id: int
    item_id: int
    qty_received: float = Field(gt=0)

@router.post("/receive")
def mark_order_received(receive_data: List[ItemReceive]):
    try:
        now = datetime.now().isoformat()
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            order_ids_updated = set()

            for item in receive_data:
                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ? AND order_id = ?
                """, (item.qty_received, now, item.item_id, item.order_id))

                cursor.execute("""
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, 'Received', ?, ?, ?)
                """, (
                    item.order_id,
                    f"Item ID {item.item_id} received: {item.qty_received}",
                    now,
                    0
                ))

                order_ids_updated.add(item.order_id)

            for order_id in order_ids_updated:
                cursor.execute("""
                    SELECT COUNT(*) FROM order_items
                    WHERE order_id = ? AND (qty_received IS NULL OR qty_received < qty_ordered)
                """, (order_id,))
                incomplete = cursor.fetchone()[0]
                if incomplete == 0:
                    cursor.execute("""
                        UPDATE orders SET status = 'Received', received_date = ?
                        WHERE id = ?
                    """, (now, order_id))

        log_event("new_orders_log.txt", {"action": "receive", "orders": list(order_ids_updated)})
        return {"status": "✅ Order(s) marked as received"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "receive"})
        raise HTTPException(status_code=500, detail=f"Failed to receive order(s): {e}")

@router.post("/upload_attachment")
async def upload_attachment(file: UploadFile, order_id: int = Form(...)):
    try:
        saved_path = UPLOAD_DIR / f"{order_id}_{file.filename}"
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, file.filename, str(saved_path), datetime.now().isoformat()))
            conn.commit()

        log_event("new_orders_log.txt", {
            "action": "attachment_uploaded",
            "order_id": order_id,
            "filename": file.filename,
            "path": str(saved_path)
        })

        return {"status": "✅ Attachment uploaded"}
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "upload"})
        raise HTTPException(status_code=500, detail=f"Failed to upload attachment: {e}")

@router.get("/pending_data")
def get_pending_orders(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier: Optional[str] = Query(None)
):
    try:
        filters = ["o.status IN ('Pending', 'Waiting for Approval')"]
        params = []

        if start_date:
            try:
                start = datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
                filters.append("DATE(o.created_date) >= DATE(?)")
                params.append(start)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid start date format")

        if end_date:
            try:
                end = datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y-%m-%d")
                filters.append("DATE(o.created_date) <= DATE(?)")
                params.append(end)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid end date format")

        if requester:
            filters.append("r.name LIKE ?")
            params.append(f"%{requester}%")

        if supplier:
            filters.append("s.name LIKE ?")
            params.append(f"%{supplier}%")

        where_clause = " AND ".join(filters)

        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT
                    o.id, o.created_date, o.order_number,
                    r.name AS requester, s.name AS supplier,
                    o.total, o.status
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                WHERE {where_clause}
                ORDER BY o.created_date DESC
            """, params)

            orders = []
            for row in cursor.fetchall():
                order = dict(row)
                if order["created_date"]:
                    dt = datetime.fromisoformat(order["created_date"])
                    order["created_date"] = dt.strftime("%d/%m/%Y")
                orders.append(order)

        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load pending orders: {e}")

```

### `backend/endpoints/requesters.py`
**(No description)**
```python
from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/requesters", tags=["requesters"])

@router.get("")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM requesters ORDER BY name")
            result = [dict(row) for row in cursor.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

### `backend/endpoints/supplier_lookup.py`
**Log file path**
```python
from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/supplier_lookup", tags=["supplier_lookup"])

# Log file path
LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "supplier_lookup_debug.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_debug(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}]\n")
        for k, v in entry.items():
            if isinstance(v, str) and len(v) > 1000:
                v = v[:1000] + "... (truncated)"
            f.write(f"{k}: {v}\n")

@router.get("")
def lookup_alternatives(query: str = Query(..., min_length=2)):
    log_debug({"💥 ROUTE HIT": f"query = {query}"})

    try:
        search_url = f"https://www.builders.co.za/search/?text={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}

        resp = requests.get(search_url, headers=headers)
        log_debug({
            "Fetched URL": search_url,
            "HTTP Status": resp.status_code,
            "First 1000 characters of response": resp.text
        })

        if resp.status_code != 200:
            raise Exception(f"Builders returned status {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for product in soup.select(".product-grid .product-tile")[:5]:
            title_el = product.select_one(".product-title")
            price_el = product.select_one(".price")
            link_el = product.select_one("a")

            if not (title_el and price_el and link_el):
                continue

            results.append({
                "title": title_el.text.strip(),
                "price": price_el.text.strip(),
                "link": "https://www.builders.co.za" + link_el.get("href")
            })

        if not results:
            raise Exception("No products matched or structure changed")

        return {"results": results}

    except Exception as e:
        log_debug({"Exception": str(e)})
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")

```

### `backend/endpoints/supplier_lookup_takealot.py`
**(No description)**
```python
from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/supplier_lookup_takealot", tags=["supplier_lookup"])

LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "takealot_lookup.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

SCRAPER_API_KEY = "f272c508f0e84b88ac0fa928d4acdda"

def log_debug(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}]\n")
        for k, v in entry.items():
            if isinstance(v, str) and len(v) > 1000:
                v = v[:1000] + "... (truncated)"
            f.write(f"{k}: {v}\n")

@router.get("")
def lookup_takealot(query: str = Query(..., min_length=2)):
    try:
        target_url = f"https://www.takealot.com/all?q={query.replace(' ', '+')}"
        scraper_url = (
            f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}"
            f"&url={target_url}"
        )

        resp = requests.get(scraper_url)
        log_debug({
            "Target URL": target_url,
            "Scraper URL": scraper_url,
            "HTTP Status": resp.status_code,
            "HTML Preview": resp.text
        })

        if resp.status_code != 200:
            raise Exception(f"ScraperAPI returned {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        product_cards = soup.select("div[data-product-id]")

        results = []
        for card in product_cards[:5]:
            title_el = card.select_one("div[data-testid='product-title']")
            price_el = card.select_one("span.currency")
            link_el = card.select_one("a[href]")

            if not (title_el and link_el):
                continue

            results.append({
                "title": title_el.text.strip(),
                "price": price_el.text.strip() if price_el else "N/A",
                "link": "https://www.takealot.com" + link_el["href"]
            })

        if not results:
            raise Exception("No products matched or structure changed")

        return {"results": results}

    except Exception as e:
        log_debug({"Exception": str(e)})
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")

```

### `backend/endpoints/ui_pages.py`
**(No description)**
```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/orders/new", response_class=HTMLResponse)
def show_new_order_form(request: Request):
    return templates.TemplateResponse("new_order.html", {"request": request})

@router.get("/orders/pending", response_class=HTMLResponse)
def show_pending_orders(request: Request):
    return templates.TemplateResponse("pending_orders.html", {"request": request})

```

### `backend/utils/__init__.py`
**Utility functions for Universal Recycling Purchase Order System**
```python
"""
Utility functions for Universal Recycling Purchase Order System
""" 
```

### `backend/utils/order_utils.py`
**Generate the next order number by splitting off any non‑digit**
```python
import re
from typing import Any, List
from datetime import datetime

def generate_order_number(current_number: str) -> str:
    """
    Generate the next order number by splitting off any non‑digit
    prefix (which can now be empty) and incrementing the numeric suffix,
    preserving zero‑padding.
    e.g. URC0001 → URC0002, PO009 → PO010, 0001 → 0002
    """
    m = re.match(r"^(\D*)(\d+)$", current_number)
    if not m:
        # if it doesn't end with digits, just append "1"
        return current_number + "1"
    prefix, digits = m.groups()
    width = len(digits)
    num = int(digits) + 1
    return f"{prefix}{str(num).zfill(width)}"


def determine_status(total: float, auth_threshold: float) -> str:
    """Return 'Awaiting Authorisation' if total > threshold, else 'Pending'."""
    return "Awaiting Authorisation" if total > auth_threshold else "Pending"


def validate_order_items(items: List[Any]) -> bool:
    """
    Ensure at least one item; qty > 0; price >= 0.
    Raises ValueError on violation.
    """
    if not items:
        raise ValueError("Order must contain at least one item")
    for item in items:
        if item.qty_ordered <= 0:
            raise ValueError("Quantity ordered must be greater than 0")
        if item.price < 0:
            raise ValueError("Price cannot be negative")
    return True

```

### `backend/scrapers/.gitkeep`
**(No description)**
```python

```

### `logs/db_activity_log.txt`
**(No description)**
```python
[2025-04-19T14:20:58.350619] init_db: {"status": "success"}
[2025-04-19T14:25:09.615221] init_db: {"status": "success"}
[2025-04-19T14:28:41.921041] init_db: {"status": "success"}
[2025-04-19T14:37:26.882988] init_db: {"status": "success"}
[2025-04-19T14:39:27.703044] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T14:39:27.703336] get_setting: {"key": "order_number_start", "result": "URC1008"}
[2025-04-19T14:39:27.703896] update_setting: {"key": "order_number_start", "value": "URC1010"}
[2025-04-19T14:39:27.704880] create_order: {"order_number": "URC1009", "requester_id": 1, "total": 1400.0, "items_count": 2}
[2025-04-19T14:42:04.162332] init_db: {"status": "success"}
[2025-04-19T14:42:23.912356] init_db: {"status": "success"}
[2025-04-19T14:42:30.739151] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T14:42:30.739332] get_setting: {"key": "order_number_start", "result": "URC1010"}
[2025-04-19T14:42:30.739873] update_setting: {"key": "order_number_start", "value": "URC1012"}
[2025-04-19T14:42:30.740663] create_order: {"order_number": "URC1011", "requester_id": 1, "total": 1400.0, "items_count": 2}
[2025-04-19T14:54:43.623841] init_db: {"status": "success"}
[2025-04-19T14:55:28.401573] init_db: {"status": "success"}
[2025-04-19T14:55:30.629586] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T14:55:30.629769] get_setting: {"key": "order_number_start", "result": "URC1012"}
[2025-04-19T14:55:30.630238] update_setting: {"key": "order_number_start", "value": "URC1014"}
[2025-04-19T14:55:30.631129] create_order: {"order_number": "URC1013", "requester_id": 1, "total": 1400.0, "items_count": 2}
[2025-04-19T15:00:26.202996] init_db: {"status": "success"}
[2025-04-19T15:04:34.886931] init_db: {"status": "success"}
[2025-04-19T15:05:36.053785] init_db: {"status": "success"}
[2025-04-19T15:07:02.165433] init_db: {"status": "success"}
[2025-04-19T15:07:04.567865] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T15:07:04.568059] get_setting: {"key": "order_number_start", "result": "URC1014"}
[2025-04-19T15:07:04.568601] update_setting: {"key": "order_number_start", "value": "URC1016"}
[2025-04-19T15:07:04.569588] create_order: {"order_number": "URC1015", "requester_id": 1, "total": 1400.0, "items_count": 2}
[2025-04-19T15:28:04.386880] init_db: {"status": "success"}
[2025-04-19T15:28:08.373448] init_db: {"status": "success"}
[2025-04-19T15:28:58.954164] init_db: {"status": "success"}
[2025-04-19T15:29:15.859282] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T15:29:15.859461] get_setting: {"key": "order_number_start", "result": "URC1016"}
[2025-04-19T15:29:15.859942] update_setting: {"key": "order_number_start", "value": "URC1018"}
[2025-04-19T15:29:15.860929] create_order: {"order_number": "URC1017", "requester_id": 1, "total": 1100.0, "items_count": 2}
[2025-04-19T15:35:41.789339] init_db: {"status": "success"}
[2025-04-19T15:35:57.486083] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T15:35:57.486372] get_setting: {"key": "order_number_start", "result": "URC1018"}
[2025-04-19T15:35:57.486861] update_setting: {"key": "order_number_start", "value": "URC1020"}
[2025-04-19T15:35:57.487800] create_order: {"order_number": "URC1019", "requester_id": 1, "total": 2000.0, "items_count": 2}
[2025-04-19T15:37:44.905947] init_db: {"status": "success"}
[2025-04-19T15:38:25.368701] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T15:38:25.368904] get_setting: {"key": "order_number_start", "result": "URC1020"}
[2025-04-19T15:38:25.369383] update_setting: {"key": "order_number_start", "value": "URC1022"}
[2025-04-19T15:38:25.370002] create_order: {"order_number": "URC1021", "requester_id": 1, "total": 20000.0, "items_count": 1}
[2025-04-19T15:40:01.587979] init_db: {"status": "success"}
[2025-04-19T15:42:44.001903] init_db: {"status": "success"}
[2025-04-19T15:42:51.554259] init_db: {"status": "success"}
[2025-04-19T15:44:05.108217] init_db: {"status": "success"}
[2025-04-19T15:44:10.144616] init_db: {"status": "success"}
[2025-04-19T15:46:09.312993] init_db: {"status": "success"}
[2025-04-19T15:46:14.381683] init_db: {"status": "success"}
[2025-04-19T15:50:18.570936] init_db: {"status": "success"}
[2025-04-19T15:50:22.982459] init_db: {"status": "success"}
[2025-04-19T15:54:03.223582] init_db: {"status": "success"}
[2025-04-19T15:55:17.006889] init_db: {"status": "success"}
[2025-04-19T15:55:55.564797] init_db: {"status": "success"}
[2025-04-19T16:00:58.097488] init_db: {"status": "success"}
[2025-04-19T16:02:19.755609] init_db: {"status": "success"}
[2025-04-19T16:02:23.570154] init_db: {"status": "success"}
[2025-04-19T16:03:59.691319] init_db: {"status": "success"}
[2025-04-19T16:04:03.353456] init_db: {"status": "success"}
[2025-04-19T16:06:46.355759] init_db: {"status": "success"}
[2025-04-19T16:06:51.707679] init_db: {"status": "success"}
[2025-04-19T16:08:31.912282] init_db: {"status": "success"}
[2025-04-19T16:08:36.954745] init_db: {"status": "success"}
[2025-04-19T16:11:34.711750] init_db: {"status": "success"}
[2025-04-19T16:11:49.998347] init_db: {"status": "success"}
[2025-04-19T16:13:43.404112] init_db: {"status": "success"}
[2025-04-19T16:13:47.199263] init_db: {"status": "success"}
[2025-04-19T16:14:48.828740] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T16:14:48.828956] get_setting: {"key": "order_number_start", "result": "URC1022"}
[2025-04-19T16:14:48.829503] update_setting: {"key": "order_number_start", "value": "URC1024"}
[2025-04-19T16:14:48.830496] create_order: {"order_number": "URC1023", "requester_id": 1, "total": 2000.0, "items_count": 2}
[2025-04-19T16:34:37.256581] init_db: {"status": "success"}
[2025-04-19T16:35:48.866331] init_db: {"status": "success"}
[2025-04-19T16:44:06.294478] init_db: {"status": "success"}
[2025-04-19T16:45:53.388846] init_db: {"status": "success"}
[2025-04-19T16:46:11.686194] init_db: {"status": "success"}
[2025-04-19T16:48:43.639732] init_db: {"status": "success"}
[2025-04-19T16:52:50.910967] init_db: {"status": "success"}
[2025-04-19T17:06:15.843472] init_db: {"status": "success"}
[2025-04-19T17:08:07.300015] init_db: {"status": "success"}
[2025-04-19T17:09:03.347514] init_db: {"status": "success"}
[2025-04-19T17:10:10.564049] init_db: {"status": "success"}
[2025-04-19T17:11:50.970429] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T17:11:50.970925] get_setting: {"key": "order_number_start", "result": "URC1024"}
[2025-04-19T17:11:50.972069] update_setting: {"key": "order_number_start", "value": "URC1026"}
[2025-04-19T17:11:50.973717] create_order: {"order_number": "URC1025", "requester_id": 1, "total": 300.0, "items_count": 1}
[2025-04-19T17:17:02.985379] init_db: {"status": "success"}
[2025-04-19T17:19:08.038389] init_db: {"status": "success"}
[2025-04-19T17:19:39.134789] init_db: {"status": "success"}
[2025-04-19T17:28:32.561824] init_db: {"status": "success"}
[2025-04-19T17:32:35.658648] get_setting: {"key": "order_number_start", "result": "URC1026"}
[2025-04-19T17:33:43.361619] get_setting: {"key": "order_number_start", "result": "URC1026"}
[2025-04-19T17:36:16.104725] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T17:36:16.106054] get_setting: {"key": "order_number_start", "result": "URC1026"}
[2025-04-19T17:36:16.108034] update_setting: {"key": "order_number_start", "value": "URC1028"}
[2025-04-19T17:36:16.111503] create_order: {"order_number": "URC1027", "requester_id": 2, "total": 1200.0, "items_count": 1}
[2025-04-19T17:36:23.525946] get_setting: {"key": "order_number_start", "result": "URC1028"}
[2025-04-19T17:36:48.886920] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T17:36:48.887578] get_setting: {"key": "order_number_start", "result": "URC1028"}
[2025-04-19T17:36:48.888773] update_setting: {"key": "order_number_start", "value": "URC1030"}
[2025-04-19T17:36:48.890470] create_order: {"order_number": "URC1029", "requester_id": 5, "total": 20.0, "items_count": 1}
[2025-04-19T17:36:51.738292] get_setting: {"key": "order_number_start", "result": "URC1030"}
[2025-04-19T17:37:29.797064] get_setting: {"key": "auth_threshold", "result": "10000"}
[2025-04-19T17:37:29.797797] get_setting: {"key": "order_number_start", "result": "URC1030"}
[2025-04-19T17:37:29.799082] update_setting: {"key": "order_number_start", "value": "URC1032"}
[2025-04-19T17:37:29.802360] create_order: {"order_number": "URC1031", "requester_id": 5, "total": 10.0, "items_count": 1}
[2025-04-19T17:37:32.198748] get_setting: {"key": "order_number_start", "result": "URC1032"}
[2025-04-20T08:08:46.970569] init_db: {"status": "success"}
[2025-04-20T08:19:21.170597] init_db: {"status": "success"}
[2025-04-20T08:20:41.901545] init_db: {"status": "success"}
[2025-04-20T08:21:34.083466] init_db: {"status": "success"}
[2025-04-20T09:26:53.402052] init_db: {"status": "success"}
[2025-04-20T09:33:01.662193] init_db: {"status": "success"}
[2025-04-20T09:44:32.506045] init_db: {"status": "success"}
[2025-04-20T09:46:01.350579] init_db: {"status": "success"}
[2025-04-20T10:18:04.761606] init_db: {"status": "success"}
[2025-04-20T12:16:57.048627] init_db: {"status": "success"}
[2025-04-20T12:40:33.765990] init_db: {"status": "success"}
[2025-04-20T12:44:07.716400] init_db: {"status": "success"}
[2025-04-20T12:44:19.033963] init_db: {"status": "success"}
[2025-04-20T12:48:24.517413] init_db: {"status": "success"}
[2025-04-20T12:51:09.261367] init_db: {"status": "success"}
[2025-04-20T12:51:20.306521] init_db: {"status": "success"}
[2025-04-20T12:52:56.362280] init_db: {"status": "success"}
[2025-04-20T12:53:01.174117] init_db: {"status": "success"}
[2025-04-20T13:20:25.126335] init_db: {"status": "success"}
[2025-04-20T13:20:37.025820] init_db: {"status": "success"}
[2025-04-20T13:20:47.744818] init_db: {"status": "success"}
[2025-04-20T13:23:27.489704] init_db: {"status": "success"}
[2025-04-20T13:23:36.851050] init_db: {"status": "success"}
[2025-04-20T13:28:48.666421] init_db: {"status": "success"}
[2025-04-20T13:28:58.496229] init_db: {"status": "success"}
[2025-04-20T13:31:34.708675] init_db: {"status": "success"}
[2025-04-20T13:31:49.776694] init_db: {"status": "success"}
[2025-04-20T13:37:56.876075] init_db: {"status": "success"}
[2025-04-20T14:04:44.716827] init_db: {"status": "success"}
[2025-04-20T14:05:07.454298] init_db: {"status": "success"}
[2025-04-20T14:06:59.593541] init_db: {"status": "success"}
[2025-04-20T14:07:05.099770] init_db: {"status": "success"}
[2025-04-20T14:35:28.443725] init_db: {"status": "success"}
[2025-04-20T14:36:27.596679] init_db: {"status": "success"}
[2025-04-20T14:45:42.267863] init_db: {"status": "success"}
[2025-04-20T14:52:55.082305] init_db: {"status": "success"}
[2025-04-20T14:58:24.173578] init_db: {"status": "success"}
[2025-04-20T15:09:22.669052] init_db: {"status": "success"}
[2025-04-20T15:12:30.951858] init_db: {"status": "success"}
[2025-04-20T15:26:00.221878] init_db: {"status": "success"}
[2025-04-20T15:45:54.288998] init_db: {"status": "success"}
[2025-04-20T15:52:23.491845] init_db: {"status": "success"}
[2025-04-20T15:57:32.410478] init_db: {"status": "success"}
[2025-04-20T16:02:19.801311] init_db: {"status": "success"}

```

### `logs/lookups_log.txt`
**(No description)**
```python
{"time": "2025-04-19T17:19:50.525099", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:19:50.525452", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:19:50.526951", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:19:50.526987", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:33:43.359209", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:33:43.359981", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:33:43.361321", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:33:43.362429", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:36:23.523549", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:36:23.524026", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:36:23.524193", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:36:23.525769", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:36:51.736563", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:36:51.737191", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:36:51.737252", "endpoint": "/items", "status": "success"}
{"time": "2025-04-19T17:36:51.739078", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:37:32.194547", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-19T17:37:32.194923", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-19T17:37:32.197866", "endpoint": "/projects", "status": "success"}
{"time": "2025-04-19T17:37:32.198621", "endpoint": "/items", "status": "success"}
{"time": "2025-04-20T14:45:45.495435", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T14:45:45.495972", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T14:52:58.436165", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T14:52:58.437142", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T14:58:27.136610", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T14:58:27.137286", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:09:25.067788", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:09:25.068794", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:12:34.020488", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:12:34.021118", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:45:58.077272", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:45:58.077585", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T15:57:37.305332", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T15:57:37.306011", "endpoint": "/suppliers", "status": "success"}
{"time": "2025-04-20T16:02:24.832425", "endpoint": "/requesters", "status": "success"}
{"time": "2025-04-20T16:02:24.832726", "endpoint": "/suppliers", "status": "success"}

```

### `logs/new_orders_log.txt`
**(No description)**
```python
[2025-04-19T14:39:27.704140] {"action": "submit_attempt", "order_data": {"order_number": "URC1009", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "PIPE001", "item_description": "Steel Pipe 2-inch", "project": "TestProject1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "JOINT002", "item_description": "Pipe Joint 2-inch", "project": "TestProject2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T14:39:27.705060] {"action": "submit_success", "order_number": "URC1009", "status": "Pending"}
[2025-04-19T14:42:30.740086] {"action": "submit_attempt", "order_data": {"order_number": "URC1011", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "TEST001", "item_description": "Steel Pipe 2-inch", "project": "TestProj1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "TEST002", "item_description": "Pipe Joint 2-inch", "project": "TestProj2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T14:42:30.740820] {"action": "submit_success", "order_number": "URC1011", "status": "Pending"}
[2025-04-19T14:55:30.630412] {"action": "submit_attempt", "order_data": {"order_number": "URC1013", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "TEST001", "item_description": "Steel Pipe 2-inch", "project": "TestProj1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "TEST002", "item_description": "Pipe Joint 2-inch", "project": "TestProj2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T14:55:30.631283] {"action": "submit_success", "order_number": "URC1013", "status": "Pending"}
[2025-04-19T14:55:30.645675] {"action": "receive", "orders": [19]}
[2025-04-19T15:07:04.568837] {"action": "submit_attempt", "order_data": {"order_number": "URC1015", "requester_id": 1, "order_note": "Pipeline test note", "note_to_supplier": "Deliver ASAP", "supplier_id": 1, "items": [{"item_code": "TEST001", "item_description": "Steel Pipe 2-inch", "project": "TestProj1", "qty_ordered": 4.0, "price": 250.0}, {"item_code": "TEST002", "item_description": "Pipe Joint 2-inch", "project": "TestProj2", "qty_ordered": 10.0, "price": 40.0}], "status": "Pending", "total": 1400.0}}
[2025-04-19T15:07:04.569746] {"action": "submit_success", "order_number": "URC1015", "status": "Pending"}
[2025-04-19T15:07:04.584492] {"action": "receive", "orders": [20]}
[2025-04-19T15:07:04.587243] {"action": "attachment_uploaded", "order_id": 20, "filename": "test_invoice.pdf", "path": "data/uploads/20_test_invoice.pdf"}
[2025-04-19T15:29:15.860120] {"action": "submit_attempt", "order_data": {"order_number": "URC1017", "requester_id": 1, "order_note": "End-to-end test order", "note_to_supplier": "Please confirm ASAP", "supplier_id": 1, "items": [{"item_code": "TST001", "item_description": "Test Widget", "project": "TEST-01", "qty_ordered": 3.0, "price": 200.0}, {"item_code": "TST002", "item_description": "Test Cable", "project": "TEST-02", "qty_ordered": 5.0, "price": 100.0}], "status": "Pending", "total": 1100.0}}
[2025-04-19T15:29:15.861078] {"action": "submit_success", "order_number": "URC1017", "status": "Pending"}
[2025-04-19T15:29:15.875787] {"action": "receive", "orders": [21]}
[2025-04-19T15:29:15.878624] {"action": "attachment_uploaded", "order_id": 21, "filename": "test_invoice.pdf", "path": "data/uploads/21_test_invoice.pdf"}
[2025-04-19T15:35:57.487040] {"action": "submit_attempt", "order_data": {"order_number": "URC1019", "requester_id": 1, "order_note": "Partial receive test", "note_to_supplier": "Split delivery test", "supplier_id": 1, "items": [{"item_code": "PART001", "item_description": "Partial Item A", "project": "SplitProjA", "qty_ordered": 10.0, "price": 100.0}, {"item_code": "PART002", "item_description": "Partial Item B", "project": "SplitProjB", "qty_ordered": 5.0, "price": 200.0}], "status": "Pending", "total": 2000.0}}
[2025-04-19T15:35:57.487956] {"action": "submit_success", "order_number": "URC1019", "status": "Pending"}
[2025-04-19T15:35:57.503247] {"action": "receive", "orders": [22]}
[2025-04-19T15:38:25.369555] {"action": "submit_attempt", "order_data": {"order_number": "URC1021", "requester_id": 1, "order_note": "Test high value order", "note_to_supplier": "Handle with care", "supplier_id": 1, "items": [{"item_code": "HIGH001", "item_description": "Premium Machine Part", "project": "TestProjX", "qty_ordered": 1.0, "price": 20000.0}], "status": "Awaiting Authorisation", "total": 20000.0}}
[2025-04-19T15:38:25.370156] {"action": "submit_success", "order_number": "URC1021", "status": "Awaiting Authorisation"}
[2025-04-19T16:14:48.829687] {"action": "submit_attempt", "order_data": {"order_number": "URC1023", "requester_id": 1, "order_note": "Partial receive test", "note_to_supplier": "Split delivery test", "supplier_id": 1, "items": [{"item_code": "PART001", "item_description": "Partial Item A", "project": "SplitProjA", "qty_ordered": 10.0, "price": 100.0}, {"item_code": "PART002", "item_description": "Partial Item B", "project": "SplitProjB", "qty_ordered": 5.0, "price": 200.0}], "status": "Pending", "total": 2000.0}}
[2025-04-19T16:14:48.830733] {"action": "submit_success", "order_number": "URC1023", "status": "Pending"}
[2025-04-19T17:11:50.972474] {"action": "submit_attempt", "order_data": {"order_number": "URC1025", "requester_id": 1, "order_note": "Browser Sim Test", "note_to_supplier": "Please rush this one", "supplier_id": 1, "items": [{"item_code": "SIM001", "item_description": "Simulated Item", "project": "PR10M", "qty_ordered": 3.0, "price": 100.0}], "status": "Pending", "total": 300.0}}
[2025-04-19T17:11:50.974002] {"action": "submit_success", "order_number": "URC1025", "status": "Pending"}
[2025-04-19T17:36:16.109144] {"action": "submit_attempt", "order_data": {"order_number": "URC1027", "requester_id": 2, "order_note": null, "note_to_supplier": "", "supplier_id": 5, "items": [{"item_code": "BEAR059", "item_description": "Bearing 51144", "project": "KA04M", "qty_ordered": 1.0, "price": 1200.0}], "status": "Pending", "total": 1200.0}}
[2025-04-19T17:36:16.112468] {"action": "submit_success", "order_number": "URC1027", "status": "Pending"}
[2025-04-19T17:36:48.889243] {"action": "submit_attempt", "order_data": {"order_number": "URC1029", "requester_id": 5, "order_note": null, "note_to_supplier": "", "supplier_id": 9, "items": [{"item_code": "BEAR180", "item_description": "Bearing Nylos Ring For 23034 Mac 4 W33 Brass Cage", "project": "PR10M", "qty_ordered": 1.0, "price": 20.0}], "status": "Pending", "total": 20.0}}
[2025-04-19T17:36:48.890998] {"action": "submit_success", "order_number": "URC1029", "status": "Pending"}
[2025-04-19T17:37:29.799798] {"action": "submit_attempt", "order_data": {"order_number": "URC1031", "requester_id": 5, "order_note": null, "note_to_supplier": "", "supplier_id": 8, "items": [{"item_code": "BEAR180", "item_description": "Bearing Nylos Ring For 23034 Mac 4 W33 Brass Cage", "project": "PR10M", "qty_ordered": 1.0, "price": 10.0}], "status": "Pending", "total": 10.0}}
[2025-04-19T17:37:29.803039] {"action": "submit_success", "order_number": "URC1031", "status": "Pending"}

```

### `logs/server.log`
**(No description)**
```python
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [70764] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'backend'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [70823] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'backend'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [70846] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'backend'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [70879] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'backend'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [70989] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
ModuleNotFoundError: No module named 'backend'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project/backend']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [71051] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
ModuleNotFoundError: No module named 'backend'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [71193] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 142
    def get_pending_orders():
IndentationError: unexpected unindent
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 13, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [71274] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 13, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [71312] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 13, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [71377] using StatReload
INFO:     Started server process [71379]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [71429] using StatReload
INFO:     Started server process [71431]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'project_testing_scripts/validate_repaired_routes.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [71431]
INFO:     Started server process [71907]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [71907]
Process SpawnProcess-3:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 9, in <module>
    from ..database import create_order, get_setting, update_setting
ImportError: cannot import name 'get_setting' from 'backend.database' (/Users/stevencohen/Projects/universal_recycling/orders_project/backend/database.py)
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [72112] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 9, in <module>
    from ..database import create_order, get_setting, update_setting
ImportError: cannot import name 'get_setting' from 'backend.database' (/Users/stevencohen/Projects/universal_recycling/orders_project/backend/database.py)
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 9, in <module>
    from ..database import create_order, get_setting, update_setting
ImportError: cannot import name 'create_order' from 'backend.database' (/Users/stevencohen/Projects/universal_recycling/orders_project/backend/database.py)
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [72176] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 3, in <module>
    from backend.endpoints import orders
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 9, in <module>
    from ..database import create_order, get_setting, update_setting
ImportError: cannot import name 'create_order' from 'backend.database' (/Users/stevencohen/Projects/universal_recycling/orders_project/backend/database.py)
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
INFO:     Started server process [72218]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [72237] using StatReload
INFO:     Started server process [72239]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [72239]
INFO:     Stopping reloader process [72237]
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [72310] using StatReload
INFO:     Started server process [72312]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61918 - "GET /orders/all HTTP/1.1" 200 OK
INFO:     127.0.0.1:61919 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:61920 - "GET /orders/print_to_file/1 HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [72312]
INFO:     Started server process [72464]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/start_server.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [72464]
INFO:     Started server process [72829]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [72871] using StatReload
INFO:     Started server process [72875]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [72935] using StatReload
INFO:     Started server process [72941]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [72941]
INFO:     Started server process [73075]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [73075]
INFO:     Started server process [73084]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [73146] using StatReload
INFO:     Started server process [73152]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62961 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:62977 - "POST /orders HTTP/1.1" 500 Internal Server Error
INFO:     127.0.0.1:62979 - "GET /orders/all HTTP/1.1" 200 OK
INFO:     127.0.0.1:63029 - "POST /orders HTTP/1.1" 400 Bad Request
WARNING:  StatReload detected changes in 'backend/utils/order_utils.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [73152]
INFO:     Started server process [73341]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [73366] using StatReload
INFO:     Started server process [73373]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:63076 - "GET /orders/all HTTP/1.1" 200 OK
INFO:     127.0.0.1:63077 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:63078 - "GET /orders/print_to_file/1 HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [73373]
INFO:     Started server process [73452]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [73452]
INFO:     Stopping reloader process [73366]
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [74235] using StatReload
INFO:     Started server process [74243]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:63144 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:63146 - "GET /orders/all HTTP/1.1" 200 OK
INFO:     127.0.0.1:63147 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:63148 - "GET /orders/print_to_file/1 HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [74243]
INFO:     Started server process [75111]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [75111]
INFO:     Started server process [75787]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [75787]
INFO:     Started server process [75953]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [75953]
INFO:     Started server process [76182]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [76182]
INFO:     Started server process [76601]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [76601]
INFO:     Started server process [77009]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [77009]
INFO:     Started server process [81011]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [81011]
INFO:     Started server process [81844]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [81844]
INFO:     Started server process [82134]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [82134]
INFO:     Started server process [89752]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [89752]
INFO:     Started server process [89765]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [89765]
INFO:     Started server process [89768]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [90262] using StatReload
INFO:     Started server process [90265]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64150 - "POST /orders HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [90265]
INFO:     Started server process [92684]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [92684]
INFO:     Stopping reloader process [90262]
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [92897] using StatReload
INFO:     Started server process [92906]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64266 - "POST /orders HTTP/1.1" 500 Internal Server Error
INFO:     127.0.0.1:64317 - "POST /orders HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [92906]
INFO:     Started server process [94337]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [94442] using StatReload
INFO:     Started server process [94447]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/insert_receive_route.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [94447]
INFO:     Started server process [95806]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/seed_static_data.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [95806]
INFO:     Started server process [2087]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/seed_static_data.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [2087]
INFO:     Started server process [3039]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_create_full_order.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [3039]
INFO:     Started server process [4214]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64995 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:65023 - "POST /orders/receive HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'scripts/seed_static_data.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [4214]
INFO:     Started server process [5719]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:65146 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:65169 - "POST /orders/receive HTTP/1.1" 200 OK
[WHATSAPP] Order PO004 exceeds threshold, notify for auth.
INFO:     127.0.0.1:65205 - "POST /orders HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [5719]
INFO:     Started server process [8753]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:65523 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:49175 - "GET /orders/received HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [8753]
INFO:     Started server process [11528]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:49209 - "GET /orders/audit/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49234 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:49236 - "GET /orders/pending?requester_id=1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49238 - "GET /orders/pending?supplier_id=1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49256 - "GET /orders/received HTTP/1.1" 200 OK
INFO:     127.0.0.1:49267 - "GET /orders/received HTTP/1.1" 200 OK
INFO:     127.0.0.1:49269 - "GET /orders/received?requester_id=1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49301 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:49303 - "GET /orders/received HTTP/1.1" 200 OK
INFO:     127.0.0.1:49305 - "GET /orders/all HTTP/1.1" 200 OK
INFO:     127.0.0.1:49307 - "GET /orders/audit/7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49309 - "GET /orders/received?requester_id=1 HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [11528]
INFO:     Started server process [13234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:49324 - "GET /orders/received?requester_id=1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49327 - "GET /orders/print_to_file/7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49393 - "GET /orders/all?from_date=2025-04-12&to_date=2025-04-17 HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [13234]
Process SpawnProcess-10:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 24, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
Process SpawnProcess-11:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
Process SpawnProcess-12:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
Process SpawnProcess-13:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
WARNING:  StatReload detected changes in 'backend/endpoints/auth.py'. Reloading...
Process SpawnProcess-14:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
Process SpawnProcess-15:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [24702] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [24885] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [25047] using StatReload
INFO:     Started server process [25049]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50235 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:50235 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [25049]
INFO:     Started server process [26715]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50350 - "GET /lookups/suppliers HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [27129] using StatReload
INFO:     Started server process [27135]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [27135]
INFO:     Started server process [27905]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [27969] using StatReload
INFO:     Started server process [27975]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50428 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:50429 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:50429 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:50433 - "GET /lookups/suppliers HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [27975]
INFO:     Started server process [29735]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50549 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:50551 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:50549 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:50549 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:52400 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [29735]
Fatal Python error: init_sys_streams: can't initialize sys standard streams
Python runtime state: core initialized
OSError: [Errno 9] Bad file descriptor

Current thread 0x000000020141c840 (most recent call first):
  <no Python frame>
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
Fatal Python error: init_sys_streams: can't initialize sys standard streams
Python runtime state: core initialized
OSError: [Errno 9] Bad file descriptor

Current thread 0x000000020141c840 (most recent call first):
  <no Python frame>
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [77463] using StatReload
INFO:     Started server process [77466]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54136 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54141 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54142 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54138 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54136 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:54194 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54198 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54200 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54202 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54196 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54194 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:54194 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [78977] using StatReload
INFO:     Started server process [78982]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54254 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54254 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54256 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54258 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54261 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:54262 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54262 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54312 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54316 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54317 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54319 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54313 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54312 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:54312 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54352 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54354 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54356 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54360 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54352 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:54358 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54358 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [78982]
INFO:     Started server process [83373]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [83373]
INFO:     Started server process [84266]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54762 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54762 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54770 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54764 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:54767 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:54769 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54769 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [84266]
INFO:     Started server process [84693]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [84693]
INFO:     Started server process [85459]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55300 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55302 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55304 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55304 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55300 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55307 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:55308 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:55400 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55402 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55407 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55400 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:55404 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55408 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:55408 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55658 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55658 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55666 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55660 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:55658 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55662 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55664 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:55695 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55698 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55701 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55696 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55695 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:55702 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:55702 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [85459]
Process SpawnProcess-6:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/lookups.py", line 1, in <module>
    @router.get("/items")
     ^^^^^^
NameError: name 'router' is not defined
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
Process SpawnProcess-7:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/lookups.py", line 1, in <module>
    @router.get("/items")
     ^^^^^^
NameError: name 'router' is not defined
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [97121] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/lookups.py", line 1, in <module>
    @router.get("/items")
     ^^^^^^
NameError: name 'router' is not defined
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [97200] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/lookups.py", line 1, in <module>
    @router.get("/items")
     ^^^^^^
NameError: name 'router' is not defined
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Started server process [97606]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [97664] using StatReload
INFO:     Started server process [97672]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55804 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55804 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55805 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:55811 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:55809 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:55808 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:55808 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [94994] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 1, in <module>
    from fastapi import FastAPI
ModuleNotFoundError: No module named 'fastapi'
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 1, in <module>
    from fastapi import FastAPI
ModuleNotFoundError: No module named 'fastapi'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [95533] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 1, in <module>
    from fastapi import FastAPI
ModuleNotFoundError: No module named 'fastapi'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [95697] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
WARNING:  StatReload detected changes in 'scripts/start_server.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [96265] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 2, in <module>
    from starlette.middleware.sessions import SessionMiddleware
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/middleware/sessions.py", line 7, in <module>
    import itsdangerous
ModuleNotFoundError: No module named 'itsdangerous'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [96376] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 6, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 14, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
WARNING:  StatReload detected changes in 'scripts/start_server.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 6, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 14, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [96545] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 6, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 14, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
WARNING:  StatReload detected changes in 'scripts/start_server.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 6, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 14, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [97140] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 6, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 14, in <module>
    templates = Jinja2Templates(directory="frontend/templates")
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/starlette/templating.py", line 96, in __init__
    assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
           ^^^^^^^^^^^^^^^^^^
AssertionError: jinja2 must be installed to use Jinja2Templates
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [97515] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 6, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
ImportError: cannot import name 'ui_pages' from 'backend.endpoints' (/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/__init__.py)
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Started server process [98044]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [98102] using StatReload
INFO:     Started server process [98108]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:56674 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:56674 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:56676 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:56678 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:56682 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:56681 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:56681 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [98955] using StatReload
INFO:     Started server process [98963]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:58208 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:58209 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:58208 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:58215 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:58214 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:58211 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:58211 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:58395 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:58395 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:58395 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:58405 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:58411 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:58410 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:58408 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [99883] using StatReload
INFO:     Started server process [99889]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:59940 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:59940 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:59941 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:59944 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:59945 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:59947 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:59947 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60102 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:60184 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:60184 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:60186 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60192 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:60189 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:60191 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:60334 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:60522 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:60522 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:60522 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:60536 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60539 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:60542 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:60541 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [1770] using StatReload
INFO:     Started server process [1777]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62488 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:62489 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62488 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:62492 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:62494 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:62495 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:62495 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:62495 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:62495 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:62488 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:62489 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:62494 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62492 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:62615 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:62615 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:62615 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:62640 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62645 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:62644 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:62646 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:62733 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:62864 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [2490] using StatReload
INFO:     Started server process [2495]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:63885 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:63949 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:63950 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:63949 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:63956 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:63954 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:63952 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:63952 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:64089 - "POST /orders HTTP/1.1" 422 Unprocessable Content
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [2495]
INFO:     Started server process [4713]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [4759] using StatReload
INFO:     Started server process [4765]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51645 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:51645 - "GET /lookups/requesters HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51646 - "GET /lookups/suppliers HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51648 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51650 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51652 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:51652 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [4765]
INFO:     Started server process [4832]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51753 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:51753 - "GET /lookups/requesters HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51754 - "GET /lookups/suppliers HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51756 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51759 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51760 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:51760 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [4878] using StatReload
INFO:     Started server process [4880]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51795 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:51795 - "GET /lookups/suppliers HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51796 - "GET /lookups/requesters HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51798 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51801 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:51802 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:51802 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [4880]
INFO:     Started server process [5471]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [5511] using StatReload
INFO:     Started server process [5516]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:53026 - "GET /orders/new HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:53026 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [5516]
INFO:     Started server process [6261]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [6261]
INFO:     Started server process [8239]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/database.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [8239]
INFO:     Started server process [9042]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/ui_pages.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [9042]
INFO:     Started server process [9608]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [9608]
INFO:     Started server process [10080]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [11256] using StatReload
INFO:     Started server process [11263]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64312 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:64313 - "POST /orders/receive HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'scripts/test_pipeline_end_to_end.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [11263]
INFO:     Started server process [11886]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [11966] using StatReload
INFO:     Started server process [11973]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:65098 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:65099 - "POST /orders/receive HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [11973]
INFO:     Started server process [13571]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [13687] using StatReload
INFO:     Started server process [13694]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51995 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:51996 - "POST /orders/receive HTTP/1.1" 200 OK
INFO:     127.0.0.1:51997 - "POST /orders/upload_attachment HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [13694]
INFO:     Started server process [14358]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/git_push_project.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [14358]
INFO:     Started server process [14916]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/git_pull_project.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [14916]
INFO:     Started server process [15056]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [15266] using StatReload
INFO:     Started server process [15273]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54987 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:54988 - "POST /orders/receive HTTP/1.1" 200 OK
INFO:     127.0.0.1:54989 - "POST /orders/upload_attachment HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'scripts/test_pipeline_end_to_end.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [15273]
INFO:     Started server process [18029]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_pipeline_end_to_end.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [18029]
INFO:     Started server process [18043]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [18170] using StatReload
INFO:     Started server process [18175]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60584 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:60585 - "POST /orders/receive HTTP/1.1" 200 OK
INFO:     127.0.0.1:60586 - "POST /orders/upload_attachment HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [19088] using StatReload
INFO:     Started server process [19095]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62253 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:62254 - "POST /orders/receive HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [19389] using StatReload
INFO:     Started server process [19395]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
[WHATSAPP] Order URC1021 exceeds threshold, notify for auth.
INFO:     127.0.0.1:62888 - "POST /orders HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [19721] using StatReload
INFO:     Started server process [19726]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [19726]
INFO:     Started server process [20086]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [20126] using StatReload
INFO:     Started server process [20133]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [20133]
INFO:     Started server process [20306]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [20339] using StatReload
INFO:     Started server process [20346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64369 - "POST /orders HTTP/1.1" 422 Unprocessable Content
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [20346]
INFO:     Started server process [20602]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [20638] using StatReload
INFO:     Started server process [20644]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64895 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:64896 - "POST /orders HTTP/1.1" 422 Unprocessable Content
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [20644]
INFO:     Started server process [21170]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [21200] using StatReload
INFO:     Started server process [21208]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [21208]
INFO:     Started server process [21701]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [21701]
INFO:     Started server process [21860]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [21965] using StatReload
INFO:     Started server process [21970]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51011 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:51012 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:51013 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [22653] using StatReload
INFO:     Started server process [22658]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [22658]
INFO:     Started server process [22848]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [22883] using StatReload
INFO:     Started server process [22888]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [22888]
INFO:     Started server process [23099]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [23134] using StatReload
INFO:     Started server process [23137]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [23137]
INFO:     Started server process [23492]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [23530] using StatReload
INFO:     Started server process [23534]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [23534]
INFO:     Started server process [23768]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [23810] using StatReload
INFO:     Started server process [23812]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [23812]
INFO:     Started server process [24219]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [24285] using StatReload
INFO:     Started server process [24287]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [24287]
INFO:     Started server process [24558]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [24593] using StatReload
INFO:     Started server process [24595]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55874 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:57975 - "POST /orders HTTP/1.1" 422 Unprocessable Content
WARNING:  StatReload detected changes in 'scripts/test_invalid_data_handling.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [24595]
INFO:     Started server process [27298]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [27490] using StatReload
INFO:     Started server process [27495]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61377 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:61378 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:61379 - "POST /orders HTTP/1.1" 422 Unprocessable Content
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [27495]
INFO:     Started server process [28577]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [28577]
INFO:     Started server process [28814]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [28880] using StatReload
INFO:     Started server process [28882]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [28882]
INFO:     Started server process [29243]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/dump_project_summary.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [29243]
INFO:     Started server process [29781]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/add_debug_validation_handler.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [29781]
INFO:     Started server process [31550]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [31550]
INFO:     Started server process [31806]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'scripts/add_debug_validation_handler.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [31806]
INFO:     Started server process [31933]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [32132] using StatReload
INFO:     Started server process [32134]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:53675 - "POST /orders HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:54033 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:54223 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:54223 - "GET /static/js/new_orders.js HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54223 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [33062] using StatReload
INFO:     Started server process [33068]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55419 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55419 - "GET /static/js/new_order.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:55419 - "GET /lookups/suppliers HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55420 - "GET /lookups/requesters HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55423 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55425 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55427 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55427 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55454 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:55454 - "GET /static/js/new_order.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:55454 - "GET /lookups/suppliers HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55455 - "GET /lookups/requesters HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55458 - "GET /lookups/items HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55459 - "GET /lookups/projects HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55461 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55461 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/lookups.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [33068]
INFO:     Started server process [33363]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [33462] using StatReload
INFO:     Started server process [33468]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:56130 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:56130 - "GET /static/js/new_order.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:56137 - "GET /orders/next_order_number HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:56131 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:56130 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:56133 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:56136 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:56136 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [33468]
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/orders.py", line 164, in <module>
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ^^^^^^^^^^
NameError: name 'UPLOAD_DIR' is not defined
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Started server process [34656]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:59337 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:59624 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:59624 - "GET /static/js/new_order.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:59624 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:59625 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:59629 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:59631 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:59625 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:59627 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:60264 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:60294 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:60294 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:60299 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:60296 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60301 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:60302 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:60410 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:60410 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:60420 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60410 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:60422 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:60426 - "GET /orders/next_order_number HTTP/1.1" 200 OK
INFO:     127.0.0.1:60425 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:60585 - "POST /orders HTTP/1.1" 200 OK
INFO:     127.0.0.1:60585 - "GET /orders/new HTTP/1.1" 200 OK
INFO:     127.0.0.1:60585 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:60599 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60605 - "GET /lookups/projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:60603 - "GET /lookups/items HTTP/1.1" 200 OK
INFO:     127.0.0.1:60606 - "GET /orders/next_order_number HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/ui_pages.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [34656]
INFO:     Started server process [51498]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54231 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:54261 - "GET /orders/pending_data HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:54272 - "GET /orders/pending_data HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [52910] using StatReload
INFO:     Started server process [52918]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54339 - "GET /orders/pending_data HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [52918]
INFO:     Started server process [53101]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54350 - "GET /orders/pending_data HTTP/1.1" 500 Internal Server Error
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [53239] using StatReload
INFO:     Started server process [53243]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54352 - "GET /orders/pending_data HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [53243]
INFO:     Started server process [61674]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [62499] using StatReload
INFO:     Started server process [62503]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54606 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:54613 - "GET /orders/pending_data HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [62503]
INFO:     Started server process [64008]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54658 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [64224] using StatReload
INFO:     Started server process [64228]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54672 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:54672 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [68427] using StatReload
INFO:     Started server process [68433]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55947 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:55947 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:55948 - "GET /favicon.ico HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [68433]
INFO:     Started server process [83764]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [83764]
Process SpawnProcess-3:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [84123] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [84362] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [84525] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [85069] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [85693] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
Process SpawnProcess-2:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [86488] using StatReload
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/opt/homebrew/Cellar/python@3.13/3.13.3/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/main.py", line 5, in <module>
    from backend.endpoints import orders, auth, lookups, ui_pages, supplier_lookup
  File "/Users/stevencohen/Projects/universal_recycling/orders_project/backend/endpoints/supplier_lookup.py", line 3, in <module>
    from bs4 import BeautifulSoup
ModuleNotFoundError: No module named 'bs4'
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [87125] using StatReload
INFO:     Started server process [87127]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
✅ supplier_lookup router loaded
INFO:     127.0.0.1:59283 - "GET /supplier_lookup?query=makita HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [87127]
INFO:     Started server process [87636]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [87685] using StatReload
INFO:     Started server process [87689]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60228 - "GET /supplier_lookup?query=makita HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [87689]
INFO:     Started server process [88241]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [88241]
INFO:     Started server process [88603]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [88653] using StatReload
INFO:     Started server process [88655]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61960 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [88655]
INFO:     Started server process [88875]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [88906] using StatReload
INFO:     Started server process [88910]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62437 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [88910]
INFO:     Started server process [92468]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [92468]
INFO:     Started server process [92501]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [92548] using StatReload
INFO:     Started server process [92551]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:53077 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [92551]
INFO:     Started server process [92914]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [92957] using StatReload
INFO:     Started server process [92963]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:53847 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [92963]
INFO:     Started server process [93650]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [93695] using StatReload
INFO:     Started server process [93701]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55244 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
INFO:     127.0.0.1:55296 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [93701]
INFO:     Started server process [94045]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [94101] using StatReload
INFO:     Started server process [94107]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:56000 - "GET /supplier_lookup_takealot/debug_html?query=laminator HTTP/1.1" 200 OK
INFO:     127.0.0.1:56000 - "GET /service-worker.js HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:56000 - "GET /service-worker.js HTTP/1.1" 404 Not Found
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [94107]
INFO:     Started server process [94926]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [94926]
INFO:     Started server process [98376]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [98446] using StatReload
INFO:     Started server process [98453]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64417 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/supplier_lookup_takealot.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [98453]
INFO:     Started server process [98702]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [98737] using StatReload
INFO:     Started server process [98743]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64925 - "GET /supplier_lookup_takealot?query=laminator HTTP/1.1" 500 Internal Server Error
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [98743]
INFO:     Started server process [2989]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [3149] using StatReload
INFO:     Started server process [3157]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:56156 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:56156 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:56156 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [4442] using StatReload
INFO:     Started server process [4449]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:58493 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:58493 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:58502 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:58500 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:58493 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:58494 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [5423] using StatReload
INFO:     Started server process [5429]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60323 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:60323 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:60328 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60323 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60326 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:60324 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:60391 - "GET /orders/pending_data?requester=Aaron HTTP/1.1" 200 OK
INFO:     127.0.0.1:60391 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [6179] using StatReload
INFO:     Started server process [6185]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61713 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:61713 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:61718 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:61713 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:61714 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:61716 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:61764 - "GET /orders/pending_data?supplier=2+Rv+Pump+Cc HTTP/1.1" 200 OK
INFO:     127.0.0.1:61764 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:61764 - "GET /orders/pending_data?requester=Aaron HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [7637] using StatReload
INFO:     Started server process [7639]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:64546 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:64546 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:64548 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:64552 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:64546 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:64550 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     127.0.0.1:64631 - "GET /orders/pending_data?requester=Aaron HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [8131] using StatReload
INFO:     Started server process [8134]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:65353 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:65353 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:65358 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:65353 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:65356 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:65354 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [9917] using StatReload
INFO:     Started server process [9923]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:52427 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:52427 - "GET /static/js/components/date_input.js HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:52428 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:52428 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [12551] using StatReload
INFO:     Started server process [12557]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:57589 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:57591 - "GET /static/js/components/date_input.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:57589 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:57595 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:57591 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:57589 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:57593 - "GET /lookups/suppliers HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/endpoints/orders.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12557]
INFO:     Started server process [13430]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [14131] using StatReload
INFO:     Started server process [14137]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60538 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:60538 - "GET /static/js/components/date_input.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:60539 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:60543 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60539 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60541 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:60538 - "GET /lookups/suppliers HTTP/1.1" 200 OK
INFO:     Will watch for changes in these directories: ['/Users/stevencohen/Projects/universal_recycling/orders_project']
INFO:     Uvicorn running on http://0.0.0.0:8004 (Press CTRL+C to quit)
INFO:     Started reloader process [14805] using StatReload
INFO:     Started server process [14811]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:60660 - "GET /orders/pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:60660 - "GET /static/js/components/date_input.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:60661 - "GET /static/js/shared_filters.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:60665 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60663 - "GET /orders/pending_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:60661 - "GET /lookups/requesters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60660 - "GET /lookups/suppliers HTTP/1.1" 200 OK

```

### `logs/server_startup.log`
**(No description)**
```python
2025-04-19 14:28:41,921 | INFO | ✅ Database initialized successfully.
2025-04-19 14:37:26,883 | INFO | ✅ Database initialized successfully.
2025-04-19 14:42:04,162 | INFO | ✅ Database initialized successfully.
2025-04-19 14:42:23,912 | INFO | ✅ Database initialized successfully.
2025-04-19 14:54:43,624 | INFO | ✅ Database initialized successfully.
2025-04-19 14:55:28,401 | INFO | ✅ Database initialized successfully.
2025-04-19 15:00:26,203 | INFO | ✅ Database initialized successfully.
2025-04-19 15:04:34,887 | INFO | ✅ Database initialized successfully.
2025-04-19 15:05:36,053 | INFO | ✅ Database initialized successfully.
2025-04-19 15:07:02,165 | INFO | ✅ Database initialized successfully.
2025-04-19 15:28:04,387 | INFO | ✅ Database initialized successfully.
2025-04-19 15:28:08,373 | INFO | ✅ Database initialized successfully.
2025-04-19 15:28:58,954 | INFO | ✅ Database initialized successfully.
2025-04-19 15:35:41,789 | INFO | ✅ Database initialized successfully.
2025-04-19 15:37:44,906 | INFO | ✅ Database initialized successfully.
2025-04-19 15:40:01,588 | INFO | ✅ Database initialized successfully.
2025-04-19 15:42:44,002 | INFO | ✅ Database initialized successfully.
2025-04-19 15:42:51,554 | INFO | ✅ Database initialized successfully.
2025-04-19 15:44:05,108 | INFO | ✅ Database initialized successfully.
2025-04-19 15:44:10,144 | INFO | ✅ Database initialized successfully.
2025-04-19 15:46:09,313 | INFO | ✅ Database initialized successfully.
2025-04-19 15:46:14,381 | INFO | ✅ Database initialized successfully.
2025-04-19 15:50:18,571 | INFO | ✅ Database initialized successfully.
2025-04-19 15:50:22,982 | INFO | ✅ Database initialized successfully.
2025-04-19 15:54:03,223 | INFO | ✅ Database initialized successfully.
2025-04-19 15:55:17,007 | INFO | ✅ Database initialized successfully.
2025-04-19 15:55:55,564 | INFO | ✅ Database initialized successfully.
2025-04-19 16:00:58,097 | INFO | ✅ Database initialized successfully.
2025-04-19 16:02:19,755 | INFO | ✅ Database initialized successfully.
2025-04-19 16:02:23,570 | INFO | ✅ Database initialized successfully.
2025-04-19 16:03:59,691 | INFO | ✅ Database initialized successfully.
2025-04-19 16:04:03,353 | INFO | ✅ Database initialized successfully.
2025-04-19 16:06:46,355 | INFO | ✅ Database initialized successfully.
2025-04-19 16:06:51,707 | INFO | ✅ Database initialized successfully.
2025-04-19 16:08:31,912 | INFO | ✅ Database initialized successfully.
2025-04-19 16:08:36,954 | INFO | ✅ Database initialized successfully.
2025-04-19 16:11:34,711 | INFO | ✅ Database initialized successfully.
2025-04-19 16:11:49,998 | INFO | ✅ Database initialized successfully.
2025-04-19 16:13:43,404 | INFO | ✅ Database initialized successfully.
2025-04-19 16:13:47,199 | INFO | ✅ Database initialized successfully.
2025-04-19 16:34:37,256 | INFO | ✅ Database initialized successfully.
2025-04-19 16:35:48,866 | INFO | ✅ Database initialized successfully.
2025-04-19 16:44:06,294 | INFO | ✅ Database initialized successfully.
2025-04-19 16:45:53,388 | INFO | ✅ Database initialized successfully.
2025-04-19 16:46:11,686 | INFO | ✅ Database initialized successfully.
2025-04-19 16:48:43,639 | INFO | ✅ Database initialized successfully.
2025-04-19 16:52:50,911 | INFO | ✅ Database initialized successfully.
2025-04-19 17:06:15,843 | INFO | ✅ Database initialized successfully.
2025-04-19 17:08:07,300 | INFO | ✅ Database initialized successfully.
2025-04-19 17:09:03,347 | INFO | ✅ Database initialized successfully.
2025-04-19 17:10:10,564 | INFO | ✅ Database initialized successfully.
2025-04-19 17:17:02,985 | INFO | ✅ Database initialized successfully.
2025-04-19 17:19:08,038 | INFO | ✅ Database initialized successfully.
2025-04-19 17:19:39,134 | INFO | ✅ Database initialized successfully.
2025-04-19 17:28:32,561 | INFO | ✅ Database initialized successfully.
2025-04-20 08:08:46,970 | INFO | ✅ Database initialized successfully.
2025-04-20 08:19:21,170 | INFO | ✅ Database initialized successfully.
2025-04-20 08:20:41,901 | INFO | ✅ Database initialized successfully.
2025-04-20 08:21:34,083 | INFO | ✅ Database initialized successfully.
2025-04-20 09:26:53,402 | INFO | ✅ Database initialized successfully.
2025-04-20 09:33:01,662 | INFO | ✅ Database initialized successfully.
2025-04-20 09:44:32,506 | INFO | ✅ Database initialized successfully.
2025-04-20 09:46:01,350 | INFO | ✅ Database initialized successfully.
2025-04-20 10:18:04,761 | INFO | ✅ Database initialized successfully.
2025-04-20 12:16:57,048 | INFO | ✅ Database initialized successfully.
2025-04-20 12:40:33,766 | INFO | ✅ Database initialized successfully.
2025-04-20 12:44:07,716 | INFO | ✅ Database initialized successfully.
2025-04-20 12:44:19,034 | INFO | ✅ Database initialized successfully.
2025-04-20 12:48:24,517 | INFO | ✅ Database initialized successfully.
2025-04-20 12:51:09,261 | INFO | ✅ Database initialized successfully.
2025-04-20 12:51:20,306 | INFO | ✅ Database initialized successfully.
2025-04-20 12:52:56,362 | INFO | ✅ Database initialized successfully.
2025-04-20 12:53:01,174 | INFO | ✅ Database initialized successfully.
2025-04-20 13:20:25,126 | INFO | ✅ Database initialized successfully.
2025-04-20 13:20:37,025 | INFO | ✅ Database initialized successfully.
2025-04-20 13:20:47,744 | INFO | ✅ Database initialized successfully.
2025-04-20 13:23:27,489 | INFO | ✅ Database initialized successfully.
2025-04-20 13:23:36,851 | INFO | ✅ Database initialized successfully.
2025-04-20 13:28:48,666 | INFO | ✅ Database initialized successfully.
2025-04-20 13:28:58,496 | INFO | ✅ Database initialized successfully.
2025-04-20 13:31:34,708 | INFO | ✅ Database initialized successfully.
2025-04-20 13:31:49,776 | INFO | ✅ Database initialized successfully.
2025-04-20 13:37:56,876 | INFO | ✅ Database initialized successfully.
2025-04-20 14:04:44,717 | INFO | ✅ Database initialized successfully.
2025-04-20 14:05:07,454 | INFO | ✅ Database initialized successfully.
2025-04-20 14:06:59,593 | INFO | ✅ Database initialized successfully.
2025-04-20 14:07:05,099 | INFO | ✅ Database initialized successfully.
2025-04-20 14:35:28,443 | INFO | ✅ Database initialized successfully.
2025-04-20 14:36:27,596 | INFO | ✅ Database initialized successfully.
2025-04-20 14:45:42,268 | INFO | ✅ Database initialized successfully.
2025-04-20 14:52:55,082 | INFO | ✅ Database initialized successfully.
2025-04-20 14:58:24,173 | INFO | ✅ Database initialized successfully.
2025-04-20 15:09:22,669 | INFO | ✅ Database initialized successfully.
2025-04-20 15:12:30,952 | INFO | ✅ Database initialized successfully.
2025-04-20 15:26:00,222 | INFO | ✅ Database initialized successfully.
2025-04-20 15:45:54,289 | INFO | ✅ Database initialized successfully.
2025-04-20 15:52:23,492 | INFO | ✅ Database initialized successfully.
2025-04-20 15:57:32,410 | INFO | ✅ Database initialized successfully.
2025-04-20 16:02:19,801 | INFO | ✅ Database initialized successfully.

```

### `logs/supplier_lookup_debug.log`
**(No description)**
```python

[]
Manual test: supplier lookup log is working


[2025-04-20T12:40:41.596788]
💥 ROUTE HIT: query = makita

[2025-04-20T12:40:44.693288]
Fetched URL: https://za.rs-online.com/web/c/?searchTerm=makita
HTTP Status: 200
First 1000 characters of response: <!DOCTYPE html><html lang="en-ZA"><head><meta charSet="utf-8" data-next-head=""/><script data-next-head="">LUX = window.LUX || {};LUX.label = "Search Results Page";</script><title data-next-head="">392 for &#x27;makita&#x27; | RS</title><meta content="width=device-width, initial-scale=1.0" name="viewport" data-next-head=""/><script id="adobe-analytics-script" type="application/javascript" data-next-head="">
    window.rs = window.rs || {"web":{"digitalData":{"customer_contact_id":null,"customer_ship_to":null,"customer_sold_to":null,"customer_type":null,"ecSystemId":"responsive","encryptedUsername":null,"isCreditAccount":null,"jobRole":null,"page_name":"search results page","page_type":"new sr","registrationDate":null,"search_browse":"SEARCH","search_cascade_order":1,"search_categories":0,"search_config":0,"search_interface_name":"","search_keyword":"makita","search_keyword_app":"makita","search_keyword_spell_corrected":"","search_language_used":"en","search_match_mode":"","search_patte... (truncated)

[2025-04-20T12:40:44.724733]
Exception: No matching results found or DOM structure changed

[2025-04-20T12:44:27.434337]
💥 ROUTE HIT: query = makita

[2025-04-20T12:44:27.968844]
Fetched URL: https://www.builders.co.za/search/?text=makita
HTTP Status: 200
First 1000 characters of response: <!DOCTYPE html>
<html lang=en data-appversion=v0.0.1578><head><link href="//accounts.google.com" rel=dns-prefetch /><title>Builders | Shop DIY, Paint and Building Materials Online</title><meta charset=utf-8 /><meta content="initial-scale=1,width=device-width,interactive-widget=resizes-content" name=viewport /><script>var __ZBE__={"uh":"aHR0cHM6Ly93d3cuYnVpbGRlcnMuY28uemE","sc":"R2g2dHVjNkw","ic":"YnVpbGRlcnM","mg":"QUl6YVN5QlI5SzVyZUFNTl9CcFFmbzBBczBfb1UwUWVEWWZpYXdv","icf":"MjU5MjU2MTgyMDIwODM2","ica":"Y28uemEuYnVpbGRlcnMubG9naW4","icg":"MzkzNDAxOTkwODY2LTFrOTBwcWIwamVlM2h1dmhpZWIybnJudjgwdTFiYjJjLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29t",};window.__ZBE__=__ZBE__;</script><link rel=dns-prefetch href="https://www.googletagmanager.com"/><link rel=dns-prefetch href="https://apps.bazaarvoice.com"/><link rel=dns-prefetch href="https://www.google-analytics.com"/><link rel=dns-prefetch href="https://www.googleoptimize.com"/><link rel=dns-prefetch href="https://maps.googleapis.com"/><script>var us... (truncated)

[2025-04-20T12:44:27.971460]
Exception: No products matched or structure changed

```

### `logs/takealot_lookup.log`
**(No description)**
```python

[2025-04-20T12:51:22.775935]
Fetched URL: https://www.takealot.com/search?searchTerm=laminator
HTTP Status: 404

[2025-04-20T12:51:22.776082]
Exception: Takealot returned status 404

[2025-04-20T12:53:16.489687]
Exception: name 'search_url' is not defined

[2025-04-20T13:20:54.092186]
Fetched URL: https://www.takealot.com/search/?search=laminator
HTTP Status: 404

[2025-04-20T13:20:54.092546]
Exception: Takealot returned status 404

[2025-04-20T13:23:42.659646]
Fetched URL: https://www.takealot.com/all?q=laminator
HTTP Status: 200

[2025-04-20T13:23:42.662571]
Exception: No products matched or structure changed

[2025-04-20T13:29:02.915905]
Fetched URL: https://www.takealot.com/all?q=laminator
HTTP Status: 200
HTML Preview:     <!doctype html>
    <html dir="ltr" lang="en">

    <head>
          <link rel="preconnect" href="https://shopfront.takealot.com" crossorigin>
  <link rel="preload" href="https://shopfront.takealot.com/static/js/app-loader.js" as="script">
  <link rel="preconnect" href="https://media.takealot.com" crossorigin>
          <title>Takealot</title>

              <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <!-- This saves us some bandwidth by saving a request favicon.ico -->
    <link rel="icon" sizes="32x32" type="image/x-icon" href="data:image/x-icon;base64,AAABAAEAEBAAAAEACABoBQAAFgAAAC\
gAAAAQAAAAIAAAAAEACAAAAAAAAAEA\
AAAAAAAAAAAAAAEAAAAAAADWrHgA1a\
p1AL16JgDmzLcAtnYSAP3//wD+//8A\
t3YSAP///wDu1ssA+vDuAPXi2wDCgz\
sAtnYRAP3//gD+//4AuHYRALd1EwD/\
//4Au3okALl2EQC4dRMAuXUTALp1Ew\
D///0At3USALh2EAC4dRIA//7/ALl2\
EAC5dRI... (truncated)

[2025-04-20T13:29:02.917653]
Exception: No products matched or structure changed

[2025-04-20T13:29:13.204128]
Fetched URL: https://www.takealot.com/all?q=laminator
HTTP Status: 200
HTML Preview:     <!doctype html>
    <html dir="ltr" lang="en">

    <head>
          <link rel="preconnect" href="https://shopfront.takealot.com" crossorigin>
  <link rel="preload" href="https://shopfront.takealot.com/static/js/app-loader.js" as="script">
  <link rel="preconnect" href="https://media.takealot.com" crossorigin>
          <title>Takealot</title>

              <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <!-- This saves us some bandwidth by saving a request favicon.ico -->
    <link rel="icon" sizes="32x32" type="image/x-icon" href="data:image/x-icon;base64,AAABAAEAEBAAAAEACABoBQAAFgAAAC\
gAAAAQAAAAIAAAAAEACAAAAAAAAAEA\
AAAAAAAAAAAAAAEAAAAAAADWrHgA1a\
p1AL16JgDmzLcAtnYSAP3//wD+//8A\
t3YSAP///wDu1ssA+vDuAPXi2wDCgz\
sAtnYRAP3//gD+//4AuHYRALd1EwD/\
//4Au3okALl2EQC4dRMAuXUTALp1Ew\
D///0At3USALh2EAC4dRIA//7/ALl2\
EAC5dRI... (truncated)

[2025-04-20T13:29:13.205841]
Exception: No products matched or structure changed

[2025-04-20T14:05:10.827015]
Target URL: https://www.takealot.com/all?q=laminator
Scraper URL: http://api.scraperapi.com?api_key=f272c508f0e84b88ac0fa928d4acdda&url=https://www.takealot.com/all?q=laminator
HTTP Status: 401
HTML Preview: Unauthorized request, please make sure your API key is valid.

[2025-04-20T14:05:10.828193]
Exception: ScraperAPI returned 401

[2025-04-20T14:07:09.512596]
Target URL: https://www.takealot.com/all?q=laminator
Scraper URL: http://api.scraperapi.com?api_key=f272c508f0e84b88ac0fa928d4acdda&url=https://www.takealot.com/all?q=laminator
HTTP Status: 401
HTML Preview: Unauthorized request, please make sure your API key is valid.

[2025-04-20T14:07:09.513530]
Exception: ScraperAPI returned 401

```

### `logs/testing_log.txt`
**(No description)**
```python
🚀 Test started
2025-04-19T15:29:15.852963 | 🚀 Running full pipeline integration test...

2025-04-19T15:29:15.861563 | ✅ Order creation succeeded
2025-04-19T15:29:15.861888 | ✅ Line items created in DB
2025-04-19T15:29:15.876258 | ⚠️ Receive response status: 200
2025-04-19T15:29:15.876300 | ⚠️ Response content: {"status":"✅ Order(s) marked as received"}
2025-04-19T15:29:15.876326 | ✅ Order receiving succeeded
2025-04-19T15:29:15.876542 | ✅ Audit trail entries exist
2025-04-19T15:29:15.878922 | ✅ Attachment uploaded
2025-04-19T15:29:15.879134 | ✅ Attachment record exists
2025-04-19T15:29:15.879169 | 
🎉 Pipeline test passed for order URC1017 (ID 21)

```

### `scripts/.DS_Store`
**(No description)**
```python
<!-- ERROR reading .DS_Store: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte -->
```

### `scripts/add_debug_validation_handler.py`
**Enhances FastAPI's default validation error responses.**
```python
#!/usr/bin/env python3
# Adds a dev-time global exception handler for clearer validation error visibility

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.encoders import jsonable_encoder
import traceback

def install_validation_handler(app):
    """
    Enhances FastAPI's default validation error responses.
    Shows raw request body and structured validation errors.
    """
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        try:
            body = await request.body()
            return JSONResponse(
                status_code=422,
                content={
                    "error": "Validation failed",
                    "path": str(request.url),
                    "detail": jsonable_encoder(exc.errors()),
                    "raw_body": body.decode("utf-8", errors="replace")
                },
            )
        except Exception as inner:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Validation failed, and logging body failed",
                    "original_error": str(exc),
                    "logging_error": traceback.format_exc()
                },
            )

```

### `scripts/clear_live_data.py`
**!/usr/bin/env python3**
```python
#!/usr/bin/env python3
import sqlite3

DB_PATH = "data/orders.db"

TABLES_TO_CLEAR = [
    "orders",
    "order_items",
    "attachments",
    "audit_trail"
]

def clear_live_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for table in TABLES_TO_CLEAR:
                print(f"Clearing table: {table}")
                cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print("✅ Live transactional data cleared successfully.")
    except Exception as e:
        print(f"❌ Failed to clear data: {e}")

if __name__ == "__main__":
    clear_live_data()


```

### `scripts/dump_project_summary.py`
**(.*?)**
```python
#!/usr/bin/env python3
import os
import sqlite3
import re
from pathlib import Path
from datetime import datetime

# --- Config ---
EXCLUDE_DIRS = {'venv', '__pycache__', '.pytest_cache'}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_MD = PROJECT_ROOT / 'project_summary.md'
DB_FILE = PROJECT_ROOT / 'data' / 'orders.db'

# --- Helpers ---
def build_tree(path: Path, prefix='') -> str:
    def _build(path, prefix, level):
        if level > 3:
            return []
        lines = []
        entries = sorted(p for p in path.iterdir() if not p.name.startswith('.') and p.name not in EXCLUDE_DIRS)
        for idx, entry in enumerate(entries):
            connector = '└── ' if idx == len(entries) - 1 else '├── '
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = '    ' if idx == len(entries) - 1 else '│   '
                lines.extend(_build(entry, prefix + extension, level + 1))
        return lines
    return f"{path}\n" + '\n'.join(_build(path, prefix, level=1))

def extract_desc(src: str) -> str:
    m = re.search(r'"""(.*?)"""', src, re.DOTALL)
    if not m:
        m = re.search(r"'''(.*?)'''", src, re.DOTALL)
    if m:
        first = m.group(1).strip().splitlines()[0]
        return first
    for line in src.splitlines():
        if line.strip().startswith('#'):
            return line.strip().lstrip('# ').strip()
    return '(No description)'

def read_src(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f"<!-- ERROR reading {path.name}: {e} -->"

def dump_db_schema(db_path: Path) -> str:
    md = "## 🗄️ Database Schema (`data/orders.db`)\n\n"
    if not db_path.exists():
        return md + "_No DB found_\n\n"
    md += "_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._\n\n"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for (tbl,) in cur.fetchall():
        md += f"### Table `{tbl}`\n"
        cur.execute(f"PRAGMA table_info({tbl});")
        for cid, name, dtype, notnull, dflt, pk in cur.fetchall():
            md += f"- `{name}` ({dtype}), pk={bool(pk)}, notnull={bool(notnull)}, default={dflt}\n"
        md += "\n"
    conn.close()
    return md

def dump_test_summary() -> str:
    md = "## 🧪 Test Coverage Summary\n\n"
    md += "| Test Script | Purpose | Status |\n"
    md += "|-------------|---------|--------|\n"
    summary = {
        "test_authorisation_threshold_trigger.py": "High-value order triggers auth flow",
        "test_invalid_data_handling.py": "Ensures invalid payloads return 422/400",
        "test_invalid_items_variants.py": "Covers malformed line item edge cases",
        "test_pipeline_end_to_end.py": "Full pipeline test: creation → receive",
        "test_receive_partial.py": "Tests partial receiving with audit tracking",
    }
    scripts_dir = PROJECT_ROOT / "scripts"
    for test_file in sorted(scripts_dir.glob("test_*.py")):
        name = test_file.name
        status = "✅"
        purpose = summary.get(name, extract_desc(read_src(test_file)))
        md += f"| `{name}` | {purpose} | {status} |\n"
    md += "\n"
    return md

def extra_sections():
    return """
## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

## ⚙️ System Settings

| Key                 | Value   |
|----------------------|---------|
| auth_threshold       | 10000   |
| order_number_start   | URC1024 |
| last_order_number    | URC000  |

## 🚦 FastAPI Endpoint Summary

| Endpoint                     | Method    | Status         |
|------------------------------|-----------|----------------|
| `/orders`                   | POST      | ✅ Implemented |
| `/orders/receive`           | POST      | ✅ Implemented |
| `/orders/next_order_number` | GET       | ✅ Implemented |
| `/attachments/upload`       | POST      | ✅ Implemented |
| `/notes`                    | GET/POST  | ✅ Implemented |
| `/audit`                    | GET       | ⏳ Pending     |
| `/orders/print`             | GET       | ⏳ Planned     |
| `/lookups/suppliers`        | GET       | ✅ Implemented |
| `/lookups/requesters`       | GET       | ✅ Implemented |
| `/lookups/projects`         | GET       | ✅ Implemented |
| `/lookups/items`            | GET       | ✅ Implemented |
"""

# --- Main dump ---
def main():
    md = []
    md.append(f"# 📦 Project Snapshot\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    md.append("## 📁 Directory Tree\n````\n" + build_tree(PROJECT_ROOT) + "\n````")
    md.append("## 📄 Source Files\n")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in sorted(files):
            p = Path(root) / f
            if p == OUTPUT_MD:
                continue
            rel = p.relative_to(PROJECT_ROOT)
            src = read_src(p)
            desc = extract_desc(src)
            md.append(f"### `{rel}`\n**{desc}**\n```python\n{src}\n```\n")
    md.append(dump_db_schema(DB_FILE))
    md.append("## 📝 Project summary\n"
              "I am busy building a Purchase Order system for Universal Recycling.\n\n"
              "**Testing Methodology:**\n"
              "- Each feature is tested in isolation (Python scripts, curl, direct sqlite3 queries)\n"
              "- No feature gets built on top of another until the one before it passes\n"
              "- Audit trails, status transitions, and data integrity are tested at every step\n"
              "- Test records are inserted programmatically, not by hand\n"
              "- UI will only be added when backend is rock solid\n\n"
              "**File Structure Summary:**\n"
              "- `backend/endpoints/orders.py` → Handles all `/orders` routes\n"
              "- `backend/database.py` → DB operations: init, insert, queries\n"
              "- `backend/utils/order_utils.py` → Helpers: status logic, validation\n"
              "- `scripts/` → Injection scripts, test runners & setup tools\n"
              "- `frontend/templates/` → Screen layouts (planned)\n"
              "- `data/orders.db` → Active SQLite file\n\n"
              "**Build Methodology:**\n"
              "- Build backend first → fully tested\n"
              "- One feature at a time → injected via `.py` scripts\n"
              "- No UI work until backend is rock solid\n"
              "- All tests confirmed via curl + Python\n"
              "- Full end-to-end integration test exists\n"
              "- Code reusability is a must (e.g. date handling, filters)\n\n"
              "**How Steven works with ChatGPT:**\n"
              "- Steven doesn’t know coding; he’s decent with terminal commands\n"
              "- He uses VS Code, wants brief error messages & clear steps\n")
    md.append(extra_sections())
    md.append(dump_test_summary())
    OUTPUT_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f"✅ Written {OUTPUT_MD}")

if __name__ == '__main__':
    main()

```

### `scripts/git_pull_project.py`
**Check for local changes**
```python
import subprocess
import os
import sys
from pathlib import Path

def run(command, desc):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr)
        sys.exit(1)

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📥 Git pull process starting...")

    # Check for local changes
    result = run(["git", "status", "--porcelain"], "Check for local changes")
    stashed = False

    if result.stdout.strip():
        print("📦 Local changes detected — stashing...")
        run(["git", "stash", "push", "-u", "-m", "Auto-stash before pull"], "Create stash")
        stashed = True

    # Pull with rebase
    run(["git", "pull", "--rebase", "origin", "main"], "Pull latest changes with rebase")

    # Restore stashed changes
    if stashed:
        print("🔁 Restoring stashed work...")
        try:
            run(["git", "stash", "pop"], "Restore stashed changes")
        except SystemExit:
            print("⚠️ Stash pop failed — resolve manually with `git stash list && git stash apply`")
            sys.exit(1)

    print("✅ Git pull completed successfully!")

if __name__ == "__main__":
    main()

```

### `scripts/git_push_project.py`
**Check if this is a Git repo**
```python
import subprocess
import os
import sys
from pathlib import Path

def run(command, desc):
    print(f"🔧 {desc}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} failed")
        print(e.stderr)
        sys.exit(1)

def main():
    repo_path = Path("/Users/stevencohen/Projects/universal_recycling/orders_project")
    os.chdir(repo_path)

    # Check if this is a Git repo
    if not (repo_path / ".git").exists():
        print("❌ Not a Git repository.")
        sys.exit(1)

    print("📦 Starting full Git sync")

    # Check current branch
    result = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], "Check current branch")
    current_branch = result.stdout.strip()
    print(f"🌿 Current branch: {current_branch}")

    # Stage all changes
    run(["git", "add", "--all"], "Stage all changes")

    # Check for staged files
    result = run(["git", "diff", "--cached", "--name-only"], "Check staged files")
    if not result.stdout.strip():
        print("✅ No changes to commit.")
        return

    # Commit
    run(["git", "commit", "-m", "📝 Auto-commit by script"], "Commit changes")

    # Pull latest with rebase
    run(["git", "pull", "--rebase", "origin", current_branch], "Pull latest changes with rebase")

    # Push changes
    run(["git", "push", "origin", current_branch], "Push changes to origin")

    print("🚀 Git sync completed successfully.")

if __name__ == "__main__":
    main()

```

### `scripts/init_db_fresh.py`
**CREATE TABLE requesters (**
```python
#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path("data/orders.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def recreate_database():
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE requesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );

        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            name TEXT,
            telephone TEXT,
            vat_number TEXT,
            registration_number TEXT,
            email TEXT,
            contact_name TEXT,
            contact_telephone TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            address_line3 TEXT,
            postal_code TEXT
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT,
            status TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            received_date TEXT,
            total REAL,
            order_note TEXT,
            note_to_supplier TEXT,
            supplier_id INTEGER REFERENCES suppliers(id),
            requester_id INTEGER REFERENCES requesters(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            item_code TEXT,
            item_description TEXT,
            project TEXT,
            qty_ordered REAL,
            qty_received REAL,
            received_date TEXT,
            price REAL,
            total REAL
        );

        CREATE TABLE attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TEXT NOT NULL
        );

        CREATE TABLE audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(id),
            action TEXT,
            details TEXT,
            action_date TEXT DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER
        );

        CREATE TABLE settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            rights TEXT NOT NULL
        );

        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT UNIQUE
        );

        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT UNIQUE,
            item_description TEXT
        );

        INSERT INTO settings (key, value) VALUES ('auth_threshold', '10000');
        INSERT INTO settings (key, value) VALUES ('order_number_start', 'PO001');
        """)

    print("✅ Database recreated with full schema.")

if __name__ == "__main__":
    recreate_database()


```

### `scripts/inject_filter_route.py`
**@router.get("/pending")**
```python
from pathlib import Path

file = Path("backend/endpoints/orders.py")
text = file.read_text()

filter_route = """
@router.get("/pending")
async def get_pending_orders():
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(\"\"\"
            SELECT 
                o.id, o.order_number, o.created_date, o.total,
                o.order_note, o.supplier_note, o.requester
            FROM orders o
            WHERE o.status = 'Pending'
        \"\"\")

        orders = cursor.fetchall()
        full_result = []

        for order in orders:
            cursor.execute(\"\"\"
                SELECT 
                    item_code, item_description, project,
                    qty_ordered, qty_received, price, total
                FROM order_items
                WHERE order_id = ?
            \"\"\", (order["id"],))
            items = [dict(row) for row in cursor.fetchall()]
            
            full_result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "created_date": order["created_date"],
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"],
                "items": items
            })

        conn.close()
        return {"pending_orders": full_result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
"""

if "/pending" not in text:
    insertion_point = text.rfind("def")
    updated = text[:insertion_point] + filter_route.strip() + "\n\n" + text[insertion_point:]
    file.write_text(updated)
    print("✅ Filter route injected into orders.py")
else:
    print("🔁 Filter route already exists in orders.py — skipping.")

```

### `scripts/insert_get_all_orders.py`
**@router.get("/all")**
```python
from pathlib import Path

TARGET_FILE = Path("backend/endpoints/orders.py")

new_route_code = '''
@router.get("/all")
async def get_all_orders():
    \"\"\"
    Retrieve all orders regardless of status.
    \"\"\"
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(\"\"\"
            SELECT id, order_number, status, created_date, total,
                   order_note, supplier_note, requester
            FROM orders
        \"\"\")

        orders = cursor.fetchall()
        conn.close()

        result = []
        for order in orders:
            result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "status": order["status"],
                "created_date": datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y"),
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"]
            })

        return {"orders": result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
'''
if __name__ == "__main__":
    content = TARGET_FILE.read_text()
    insert_point = content.rfind('@router.get')
    updated = content[:insert_point] + new_route_code.strip() + '\n\n' + content[insert_point:]
    TARGET_FILE.write_text(updated)
    print("✅ /all orders route injected.")

```

### `scripts/insert_next_order_number_route.py`
**@router.get("/next_order_number")**
```python
from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

new_route = """
@router.get("/next_order_number")
async def get_next_order_number():
    from ..database import get_setting
    current = get_setting("order_number_start")
    return {"next_order_number": current}
"""

if __name__ == "__main__":
    content = TARGET.read_text()
    inject_index = content.rfind("@router.get")
    updated = content[:inject_index] + new_route.strip() + "\n\n" + content[inject_index:]
    TARGET.write_text(updated)
    print("✅ /orders/next_order_number route injected.")

```

### `scripts/insert_pending_route.py`
**Retrieve all pending orders, each with full item breakdown.**
```python
from pathlib import Path

# Target: orders endpoint file
TARGET_FILE = Path("backend/endpoints/orders.py")

# Code to inject
pending_route_code = '''
@router.get("/pending")
async def get_pending_orders():
    """
    Retrieve all pending orders, each with full item breakdown.
    """
    try:
        conn = sqlite3.connect("data/orders.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                o.id, o.order_number, o.created_date, o.total,
                o.order_note, o.supplier_note, o.requester
            FROM orders o
            WHERE o.status = 'Pending'
        """)

        orders = cursor.fetchall()
        full_result = []

        for order in orders:
            cursor.execute("""
                SELECT 
                    item_code, item_description, project,
                    qty_ordered, qty_received, price, total
                FROM order_items
                WHERE order_id = ?
            """, (order["id"],))
            items = [dict(row) for row in cursor.fetchall()]
            
            full_result.append({
                "id": order["id"],
                "order_number": order["order_number"],
                "created_date": datetime.fromisoformat(order["created_date"]).strftime("%d/%m/%Y"),
                "total": order["total"],
                "order_note": order["order_note"],
                "supplier_note": order["supplier_note"],
                "requester": order["requester"],
                "items": items
            })

        conn.close()
        return {"pending_orders": full_result}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
'''

if __name__ == "__main__":
    content = TARGET_FILE.read_text()
    split_point = content.rfind('@router.get')
    updated = content[:split_point] + pending_route_code.strip()
    TARGET_FILE.write_text(updated)
    print("✅ /pending route injected successfully.")

```

### `scripts/insert_print_route.py`
**from fastapi.responses import HTMLResponse**
```python
from pathlib import Path
import sqlite3
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from starlette.requests import Request

TARGET = Path("../backend/endpoints/orders.py")

injected_code = """
from fastapi.responses import HTMLResponse
from starlette.requests import Request

@router.get("/orders/print/{order_id}", response_class=HTMLResponse)
def print_order(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute(\"\"\"
                SELECT order_number, status, created_date, received_date, total,
                       order_note, supplier_note, requester
                FROM orders
                WHERE id = ?
            \"\"\", (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            order_dict = {
                "order_number": order[0],
                "status": order[1],
                "created_date": order[2],
                "received_date": order[3],
                "total": order[4],
                "order_note": order[5],
                "supplier_note": order[6],
                "requester": order[7],
            }

            cursor.execute(\"\"\"
                SELECT item_code, item_description, project, qty_ordered, price, total
                FROM order_items
                WHERE order_id = ?
            \"\"\", (order_id,))
            order_items = cursor.fetchall()

        return templates.TemplateResponse("print_template.html", {
            "request": Request({}),
            "order": order_dict,
            "items": order_items
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating printable order: {str(e)}")
"""

if __name__ == "__main__":
    text = TARGET.read_text()
    insert_index = text.rfind("@router.get")
    updated_code = text[:insert_index] + injected_code.strip() + "\n\n" + text[insert_index:]
    TARGET.write_text(updated_code)
    print("✅ /orders/print/{order_id} route injected.")

```

### `scripts/insert_receive_route.py`
**UPDATE order_items**
```python
#!/usr/bin/env python3
from pathlib import Path

orders_py = Path("backend/endpoints/orders.py")

route_code = '''
@router.post("/receive")
def mark_order_received(receive_data: List[dict]):
    try:
        now = datetime.now().isoformat()
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()

            order_ids_updated = set()
            for item in receive_data:
                order_id = item["order_id"]
                item_id = item["item_id"]
                qty_received = item["qty_received"]

                cursor.execute("""
                    UPDATE order_items
                    SET qty_received = ?, received_date = ?
                    WHERE id = ? AND order_id = ?
                """, (qty_received, now, item_id, order_id))

                cursor.execute("""
                    INSERT INTO audit_trail (order_id, action, details, action_date, user_id)
                    VALUES (?, 'Received', ?, ?, ?)
                """, (order_id, f"Item ID {item_id} received: {qty_received}", now, 0))

                order_ids_updated.add(order_id)

            for order_id in order_ids_updated:
                cursor.execute("""
                    SELECT COUNT(*) FROM order_items
                    WHERE order_id = ? AND (qty_received IS NULL OR qty_received < qty_ordered)
                """, (order_id,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        UPDATE orders
                        SET status = 'Received', received_date = ?
                        WHERE id = ?
                    """, (now, order_id))

        return {"status": "✅ Order(s) marked as received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to receive order: {e}")
'''

if orders_py.exists():
    code = orders_py.read_text()
    if "/receive" in code:
        print("⚠️  Route already exists in orders.py — skipping.")
    else:
        with open(orders_py, "a") as f:
            f.write("\n" + route_code.strip() + "\n")
        print("✅ /receive route injected into orders.py")
else:
    print("❌ backend/endpoints/orders.py not found")

```

### `scripts/integration_tests.py`
**Requisition System Integration Test Suite**
```python
"""
Requisition System Integration Test Suite
----------------------------------------
A comprehensive test suite that validates the full requisition pipeline
from login through submission to database storage and frontend display.
"""

import os
import sys
import json
import time
import requests
import unittest
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import uuid
import re

# Install required packages with:
# pip install selenium requests webdriver-manager

class TestResult:
    """Stores the result of a single test case with before/after state"""
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now()
        self.end_time = None
        self.passed = False
        self.before_state = {}
        self.after_state = {}
        self.assertions = []
        self.error = None
        self.stacktrace = None
    
    def add_assertion(self, assertion_name, passed, expected=None, actual=None):
        """Add a single assertion result"""
        self.assertions.append({
            "name": assertion_name,
            "passed": passed,
            "expected": expected,
            "actual": actual
        })
    
    def set_before_state(self, state):
        """Set the before state snapshot"""
        self.before_state = state
    
    def set_after_state(self, state):
        """Set the after state snapshot"""
        self.after_state = state
    
    def set_error(self, error, stacktrace):
        """Record an error with stacktrace"""
        self.error = str(error)
        self.stacktrace = stacktrace
    
    def finalize(self, passed):
        """Mark the test as complete with final result"""
        self.passed = passed
        self.end_time = datetime.now()
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else None,
            "passed": self.passed,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "assertions": self.assertions,
            "error": self.error,
            "stacktrace": self.stacktrace
        }
    
    def __str__(self):
        """Format the test result for display"""
        result = f"Test: {self.name}\n"
        result += f"Status: {'PASSED' if self.passed else 'FAILED'}\n"
        result += f"Duration: {(self.end_time - self.start_time).total_seconds():.2f}s\n\n"
        
        # Print before state
        result += "Before State:\n"
        result += json.dumps(self.before_state, indent=2) + "\n\n"
        
        # Print after state
        result += "After State:\n"
        result += json.dumps(self.after_state, indent=2) + "\n\n"
        
        # Print assertions
        result += "Assertions:\n"
        for assertion in self.assertions:
            status = "✓" if assertion["passed"] else "✗"
            result += f"{status} {assertion['name']}\n"
            if not assertion["passed"]:
                result += f"  Expected: {assertion['expected']}\n"
                result += f"  Actual:   {assertion['actual']}\n"
        
        # Print error
        if self.error:
            result += "\nError:\n"
            result += self.error + "\n\n"
            result += "Stacktrace:\n"
            result += self.stacktrace + "\n"
        
        return result

class ValidationSuite:
    """Collects and summarizes multiple test results"""
    def __init__(self):
        self.results = []
    
    def add_result(self, result):
        """Add a test result to the suite"""
        self.results.append(result)
    
    def print_summary(self):
        """Print a summary of all test results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print("\n===== VALIDATION SUMMARY =====")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.2f}%")
        print("=============================\n")
        
        for result in self.results:
            print(result)
            print("-----------------------------\n")
    
    def has_failures(self):
        """Check if any tests failed"""
        return any(not r.passed for r in self.results)

class DatabaseHelper:
    """Helper for database operations via API"""
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_requisition_count(self):
        """Get the total number of requisitions"""
        response = requests.get(f"{self.base_url}/api/requisitions")
        if response.status_code == 200:
            return len(response.json())
        return 0
    
    def get_transaction_count(self):
        """Get the total number of transactions"""
        response = requests.get(f"{self.base_url}/api/transactions")
        if response.status_code == 200:
            return len(response.json())
        return 0
    
    def get_requisition_by_order_number(self, order_number):
        """Get a requisition by its order number"""
        response = requests.get(f"{self.base_url}/api/requisitions")
        if response.status_code == 200:
            requisitions = response.json()
            return [r for r in requisitions if r.get("order_number") == order_number]
        return []
    
    def get_requisition_items(self, requisition_id):
        """Get all items for a requisition"""
        response = requests.get(f"{self.base_url}/api/requisition_items/{requisition_id}")
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_transaction_by_order_number(self, order_number):
        """Get a transaction by its order number"""
        response = requests.get(f"{self.base_url}/api/transactions")
        if response.status_code == 200:
            transactions = response.json()
            return [t for t in transactions if t.get("order_number") == order_number]
        return []
    
    def get_next_order_number(self):
        """Get the next order number from settings"""
        response = requests.get(f"{self.base_url}/api/settings/order_number_start")
        if response.status_code == 200:
            data = response.json()
            return data.get("order_number_start", 1000)
        return 1000

class RequisitionSystemTests:
    """Main test suite for the requisition system"""
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.validation = ValidationSuite()
        
        # Setup WebDriver for browser automation
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)
        
        # Setup database helper
        self.db = DatabaseHelper(self.base_url)
    
    def teardown(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
    
    def login(self, username="Steven"):
        """Log in to the application"""
        self.driver.get(self.base_url)
        
        try:
            # Check if already logged in
            if "currentUser" in self.driver.page_source:
                current_user = self.driver.find_element(By.ID, "currentUser").text
                if username in current_user:
                    return True
            
            # Enter username
            username_input = self.driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys(username)
            
            # Submit form
            login_form = self.driver.find_element(By.ID, "loginForm")
            login_form.submit()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "mainApp"))
            )
            
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def fill_requisition_form(self, data):
        """Fill out the requisition form with test data"""
        # Navigate to form tab
        self.driver.get(self.base_url)
        
        # Wait for page to fully load
        time.sleep(5)
        print("Page loaded, checking for new requisition tab...")
        
        # Set a longer wait time
        wait = WebDriverWait(self.driver, 30)
        
        # Ensure we're on the new requisition tab
        try:
            # Try explicit wait first
            print("Waiting for new requisition tab button...")
            new_req_tab = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('new-requisition')\"]"))
            )
            print("Found tab button, clicking...")
            new_req_tab.click()
            print("Tab button clicked")
        except Exception as e:
            print(f"Error clicking tab button: {e}")
            # If direct click fails, try JavaScript click as fallback
            try:
                print("Attempting fallback method to find tab...")
                new_req_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('new-requisition')\"]")
                print("Found tab via fallback, executing JavaScript click...")
                self.driver.execute_script("arguments[0].click();", new_req_tab)
                print("JavaScript click executed")
            except Exception as e2:
                print(f"Fallback method failed: {e2}")
                # Direct JavaScript call to the function as last resort
                print("Last resort: directly calling showTab function...")
                self.driver.execute_script("showTab('new-requisition');")
                print("showTab function called directly")
        
        # Wait for the form to be visible
        print("Waiting for requisition form to become visible...")
        wait.until(
            EC.visibility_of_element_located((By.ID, "requisitionForm"))
        )
        print("Form is now visible")
        
        # Fill form fields
        if "requestDate" in data:
            print("Setting request date...")
            date_input = wait.until(
                EC.element_to_be_clickable((By.ID, "requestDate"))
            )
            date_input.clear()
            date_input.send_keys(data["requestDate"])
            print("Request date set")
        
        if "requester" in data:
            print("Setting requester...")
            self.driver.find_element(By.ID, "requester").send_keys(data["requester"])
            print("Requester set")
        
        if "supplier" in data:
            print("Setting supplier...")
            self.driver.find_element(By.ID, "supplier").send_keys(data["supplier"])
            print("Supplier set")
        
        if "note" in data:
            print("Setting note...")
            self.driver.find_element(By.ID, "note").send_keys(data["note"])
            print("Note set")
        
        # Fill stock items
        print(f"About to fill {len(data.get('items', []))} stock items...")
        for i, item in enumerate(data.get("items", [])):
            print(f"Filling stock item {i+1}...")
            # If not first item, add new row
            if i > 0:
                print("Adding new row...")
                add_button = self.driver.find_elements(By.CSS_SELECTOR, ".action-square.green-square")[0]
                add_button.click()
                print("New row added")
            
            # Get all stock item rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, ".stock-item-row")
            row = rows[i]
            
            # Select stock code
            print("Selecting stock code...")
            stock_select = row.find_element(By.CSS_SELECTOR, "select[name='stockCode[]']")
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='stockCode[]'] option:nth-child(2)"))
            )
            options = stock_select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if item.get("stockCode", "") in option.text:
                    option.click()
                    print(f"Selected stock code: {option.text}")
                    break
            else:
                # If not found, pick first non-empty
                for option in options:
                    if option.get_attribute("value"):
                        option.click()
                        print(f"Selected first available stock code: {option.text}")
                        break
            
            # Select project code
            print("Selecting project code...")
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='projectCode[]']"))
            )
            project_select = row.find_element(By.CSS_SELECTOR, "select[name='projectCode[]']")
            options = project_select.find_elements(By.TAG_NAME, "option")
            for option in options:
                if option.get_attribute("value"):
                    option.click()
                    print(f"Selected project code: {option.text}")
                    break
            
            # Select sub category (wait for it to populate)
            print("Waiting for subcategories to populate...")
            try:
                wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='subCategory[]'] option:nth-child(2)"))
                )
                subcat_select = row.find_element(By.CSS_SELECTOR, "select[name='subCategory[]']")
                options = subcat_select.find_elements(By.TAG_NAME, "option")
                if len(options) > 1:
                    options[1].click()
                    print(f"Selected subcategory: {options[1].text}")
            except Exception as e:
                print(f"Error selecting subcategory: {e}, continuing anyway...")
            
            # Fill units and price
            print("Setting units...")
            units_input = row.find_element(By.CSS_SELECTOR, "input[name='units[]']")
            units_input.clear()
            units_input.send_keys(str(item.get("units", 1)))
            print(f"Units set to {item.get('units', 1)}")
            
            print("Setting price...")
            price_input = row.find_element(By.CSS_SELECTOR, "input[name='price[]']")
            price_input.clear()
            price_input.send_keys(str(item.get("price", 100)))
            print(f"Price set to {item.get('price', 100)}")
            
        print("Form filling complete")
    
    def submit_form(self, expect_alert=True):
        """Submit the requisition form"""
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#requisitionForm button[type='submit']")
        submit_button.click()
        
        if expect_alert:
            try:
                # Wait for alert and accept it
                WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                return alert_text
            except TimeoutException:
                return None
        return None
    
    def check_session_active(self):
        """Check if user session is still active"""
        try:
            # Try to access currentUser element - should be visible if logged in
            current_user = self.driver.find_element(By.ID, "currentUser").text
            return len(current_user) > 0
        except:
            # If element not found, session likely ended
            return False
    
    def check_login_screen_visible(self):
        """Check if login screen is visible (user logged out)"""
        try:
            login_screen = self.driver.find_element(By.ID, "loginScreen")
            return login_screen.is_displayed()
        except:
            return False
    
    def check_transaction_in_audit_trail(self, order_number):
        """Check if a transaction appears in the audit trail tab"""
        # Navigate to audit trail tab
        self.driver.get(self.base_url)
        
        # Wait for page to fully load
        time.sleep(2)
        
        try:
            # Try explicit wait first
            audit_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('audit-trail')\"]"))
            )
            audit_tab.click()
        except:
            # If direct click fails, try JavaScript click as fallback
            try:
                audit_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('audit-trail')\"]")
                self.driver.execute_script("arguments[0].click();", audit_tab)
            except:
                # Direct JavaScript call to the function as last resort
                self.driver.execute_script("showTab('audit-trail');")
        
        # Wait for data to load
        time.sleep(2)
        
        # Check if transaction is in table
        try:
            transactions_table = self.driver.find_element(By.ID, "transactionsTableBody")
            rows = transactions_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 1 and order_number in cells[1].text:
                    return True
            return False
        except:
            return False
    
    def test_standard_requisition_submission(self):
        """
        Test a standard requisition submission flow from end to end
        
        Validates:
        - Login works
        - Form submission succeeds
        - Requisition is saved to database
        - Items are saved to database
        - Transaction is created
        - Order number increments
        - Session remains active
        - Audit trail shows the transaction
        """
        test_result = TestResult("Standard Requisition Submission")
        
        try:
            # Login
            logged_in = self.login()
            test_result.add_assertion("Login successful", logged_in)
            
            if not logged_in:
                raise Exception("Failed to login, cannot continue test")
            
            # Get initial state
            next_order_number = self.db.get_next_order_number()
            formatted_order_number = f"ORD-{next_order_number}"
            req_count_before = self.db.get_requisition_count()
            txn_count_before = self.db.get_transaction_count()
            
            before_state = {
                "next_order_number": next_order_number,
                "requisition_count": req_count_before,
                "transaction_count": txn_count_before,
                "logged_in": True
            }
            test_result.set_before_state(before_state)
            
            # Fill form with test data
            test_data = {
                "requestDate": "12/04/2024",
                "requester": "Integration Test",
                "supplier": "Validation Supplier",
                "note": "End-to-end integration test",
                "items": [
                    {"stockCode": "AB", "units": 5, "price": 100},
                    {"stockCode": "CD", "units": 2, "price": 200}
                ]
            }
            self.fill_requisition_form(test_data)
            
            # Submit form
            alert_text = self.submit_form()
            form_submitted = alert_text and "success" in alert_text.lower()
            test_result.add_assertion("Form submitted successfully", form_submitted, 
                                     "Alert with success message", alert_text)
            
            # Wait for processing
            time.sleep(3)
            
            # Check if still logged in
            still_logged_in = self.check_session_active()
            logged_out = self.check_login_screen_visible()
            test_result.add_assertion("Session remained active", still_logged_in,
                                     "User still logged in", f"Logged in: {still_logged_in}, Login screen visible: {logged_out}")
            
            # Get updated state from database
            req_count_after = self.db.get_requisition_count()
            txn_count_after = self.db.get_transaction_count()
            current_order_number = self.db.get_next_order_number()
            
            # Check requisition in database
            requisitions = self.db.get_requisition_by_order_number(formatted_order_number)
            requisition_created = len(requisitions) > 0
            test_result.add_assertion("Requisition created in database", requisition_created,
                                     "One requisition record", len(requisitions))
            
            if requisition_created:
                requisition = requisitions[0]
                requisition_id = requisition["id"]
                
                # Check requisition fields
                test_result.add_assertion("Requisition has correct order number", 
                                         requisition["order_number"] == formatted_order_number,
                                         formatted_order_number, requisition["order_number"])
                
                test_result.add_assertion("Requisition has correct requester", 
                                         requisition["requester"] == test_data["requester"],
                                         test_data["requester"], requisition["requester"])
                
                test_result.add_assertion("Requisition has correct supplier", 
                                         requisition["supplier"] == test_data["supplier"],
                                         test_data["supplier"], requisition["supplier"])
                
                test_result.add_assertion("Requisition has correct note", 
                                         requisition["supplier_note"] == test_data["note"],
                                         test_data["note"], requisition["supplier_note"])
                
                # Check requisition items
                req_items = self.db.get_requisition_items(requisition_id)
                items_created = len(req_items) == len(test_data["items"])
                test_result.add_assertion("All requisition items created", items_created,
                                         len(test_data["items"]), len(req_items))
                
                # Calculate expected total value
                expected_total = sum(item["units"] * item["price"] for item in test_data["items"])
                test_result.add_assertion("Requisition has correct total value", 
                                         float(requisition["total_order_value"]) == expected_total,
                                         expected_total, float(requisition["total_order_value"]))
                
                # Check transaction in database
                transactions = self.db.get_transaction_by_order_number(formatted_order_number)
                transaction_created = len(transactions) > 0
                test_result.add_assertion("Transaction created in database", transaction_created,
                                         "One transaction record", len(transactions))
                
                if transaction_created:
                    transaction = transactions[0]
                    
                    # Check transaction fields
                    test_result.add_assertion("Transaction has correct order number", 
                                             transaction["order_number"] == formatted_order_number,
                                             formatted_order_number, transaction["order_number"])
                    
                    test_result.add_assertion("Transaction has correct type", 
                                             transaction["transaction_type"] == "Order Placed",
                                             "Order Placed", transaction["transaction_type"])
                    
                    test_result.add_assertion("Transaction has correct amount", 
                                             float(transaction["amount"]) == expected_total,
                                             expected_total, float(transaction["amount"]))
                    
                    test_result.add_assertion("Transaction has correct user", 
                                             transaction["user"] == test_data["requester"],
                                             test_data["requester"], transaction["user"])
                    
                    test_result.add_assertion("Transaction has correct status", 
                                             transaction["status"] in ["Pending", "pending"],
                                             "Pending", transaction["status"])
            
            # Check if order number incremented
            order_number_incremented = current_order_number == next_order_number + 1
            test_result.add_assertion("Order number incremented", order_number_incremented,
                                     next_order_number + 1, current_order_number)
            
            # Check if transaction appears in audit trail
            in_audit_trail = self.check_transaction_in_audit_trail(formatted_order_number)
            test_result.add_assertion("Transaction visible in audit trail", in_audit_trail,
                                     "Transaction in audit table", in_audit_trail)
            
            # Record final state
            after_state = {
                "next_order_number": current_order_number,
                "requisition_count": req_count_after,
                "transaction_count": txn_count_after,
                "requisition_count_delta": req_count_after - req_count_before,
                "transaction_count_delta": txn_count_after - txn_count_before,
                "still_logged_in": still_logged_in,
                "requisition": requisitions[0] if requisitions else None,
                "transaction": transactions[0] if transactions else None,
                "items_count": len(req_items) if 'req_items' in locals() else 0
            }
            test_result.set_after_state(after_state)
            
            # Determine overall test result
            test_passed = all(assertion["passed"] for assertion in test_result.assertions)
            test_result.finalize(test_passed)
            
        except Exception as e:
            # Capture full stacktrace for debugging
            error_trace = traceback.format_exc()
            test_result.set_error(e, error_trace)
            test_result.finalize(False)
        
        finally:
            # Add result to validation suite
            self.validation.add_result(test_result)
            
        return test_result
    
    def test_session_persistence(self):
        """
        Test that user session persists after form submission
        
        Validates:
        - User remains logged in after submission
        - No redirect to login screen
        - User can navigate to other tabs after submission
        """
        test_result = TestResult("Session Persistence")
        
        try:
            # Login
            logged_in = self.login()
            test_result.add_assertion("Login successful", logged_in)
            
            if not logged_in:
                raise Exception("Failed to login, cannot continue test")
            
            # Get user info before submission
            current_user_before = self.driver.find_element(By.ID, "currentUser").text
            
            before_state = {
                "logged_in": logged_in,
                "username": current_user_before
            }
            test_result.set_before_state(before_state)
            
            # Fill form
            test_data = {
                "requestDate": "12/04/2024",
                "requester": "Session Test",
                "supplier": "Persistence Co",
                "note": "Testing session persistence",
                "items": [
                    {"stockCode": "AB", "units": 1, "price": 25}
                ]
            }
            self.fill_requisition_form(test_data)
            
            # Submit form
            alert_text = self.submit_form()
            form_submitted = alert_text and "success" in alert_text.lower()
            test_result.add_assertion("Form submitted successfully", form_submitted)
            
            # Wait for processing
            time.sleep(3)
            
            # Check if still logged in
            is_logged_in = self.check_session_active()
            login_screen_visible = self.check_login_screen_visible()
            
            test_result.add_assertion("User still logged in after submission", is_logged_in,
                                     "User logged in", is_logged_in)
            
            test_result.add_assertion("Login screen not shown after submission", not login_screen_visible,
                                     "Login screen hidden", login_screen_visible)
            
            # Try navigating to another tab
            try:
                pending_tab = self.driver.find_element(By.CSS_SELECTOR, "button.tab-button[onclick=\"showTab('pending')\"]")
                pending_tab.click()
                
                # Wait for tab content to load
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "pending"))
                )
                
                pending_tab_visible = True
            except:
                pending_tab_visible = False
            
            test_result.add_assertion("Can navigate to other tabs after submission", pending_tab_visible)
            
            # If still logged in, get current user info
            current_user_after = None
            if is_logged_in:
                try:
                    current_user_after = self.driver.find_element(By.ID, "currentUser").text
                except:
                    current_user_after = None
            
            test_result.add_assertion("Username preserved after submission", 
                                     current_user_after == current_user_before,
                                     current_user_before, current_user_after)
            
            after_state = {
                "logged_in": is_logged_in,
                "username": current_user_after,
                "login_screen_visible": login_screen_visible,
                "navigation_functional": pending_tab_visible
            }
            test_result.set_after_state(after_state)
            
            # Determine overall test result
            test_passed = all(assertion["passed"] for assertion in test_result.assertions)
            test_result.finalize(test_passed)
            
        except Exception as e:
            # Capture full stacktrace for debugging
            error_trace = traceback.format_exc()
            test_result.set_error(e, error_trace)
            test_result.finalize(False)
        
        finally:
            # Add result to validation suite
            self.validation.add_result(test_result)
            
        return test_result
    
    def run_all_tests(self):
        try:
            # Run all tests in sequence
            print("Starting Standard Requisition Submission test...")
            self.test_standard_requisition_submission()
            
            print("Starting Session Persistence test...")
            self.test_session_persistence()
            
            # Print summary
            self.validation.print_summary()
            
            return not self.validation.has_failures()
        finally:
            self.teardown()

if __name__ == "__main__":
    print("Starting Requisition System Integration Tests...")
    tests = RequisitionSystemTests()
    success = tests.run_all_tests()
    sys.exit(0 if success else 1) 
```

### `scripts/prepare_lookup_tables.py`
**CREATE TABLE IF NOT EXISTS suppliers (**
```python
import sqlite3

conn = sqlite3.connect("data/orders.db")
cursor = conn.cursor()

# Create suppliers table with full structure
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    name TEXT,
    tel TEXT,
    vat_number TEXT,
    registration_number TEXT,
    email TEXT,
    contact_name TEXT,
    contact_tel TEXT,
    address_line_1 TEXT,
    address_line_2 TEXT,
    address_line_3 TEXT,
    postal_code TEXT
)
""")

# Create projects table if missing
cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, project_code TEXT NOT NULL UNIQUE)")

# Create items table if missing
cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, item_code TEXT NOT NULL UNIQUE, item_description TEXT)")

# Create users table if missing
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rights TEXT NOT NULL CHECK(rights IN ('View', 'Edit'))
)
""")

# Insert blank placeholder suppliers
for _ in range(3):
    cursor.execute("""
    INSERT INTO suppliers (
        account_number, name, tel, vat_number, registration_number,
        email, contact_name, contact_tel, address_line_1, address_line_2,
        address_line_3, postal_code
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple("" for _ in range(12)))

conn.commit()
conn.close()
print("✅ Lookup tables prepared with full supplier structure.")

```

### `scripts/repair_orders_routes.py`
**SELECT o.*, r.name AS requester**
```python
from pathlib import Path

file = Path("backend/endpoints/orders.py")
routes_code = '''from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import sqlite3
from datetime import datetime
from pathlib import Path

router = APIRouter()

@router.get("/all")
def get_all_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {e}")

@router.get("/pending")
def get_pending_orders():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.status = 'Pending'
            """)
            orders = [dict(row) for row in cursor.fetchall()]
        return {"pending_orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending orders: {e}")

@router.get("/print_to_file/{order_id}")
def print_order_to_file(order_id: int):
    output_path = Path("data/printouts") / f"order_{order_id}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            cursor.execute("""
                SELECT * FROM order_items
                WHERE order_id = ?
            """, (order_id,))
            items = cursor.fetchall()

        lines = [
            f"Order Number: {order['order_number']}",
            f"Status: {order['status']}",
            f"Created: {order['created_date']}",
            f"Requester: {order['requester']}",
            f"Total: {order['total']}",
            f"Supplier Note: {order['supplier_note'] or 'None'}",
            f"Order Note: {order['order_note'] or 'None'}",
            "",
            "Items:"
        ]
        for item in items:
            lines.append(
                f"- {item[2]} | {item[3]} | Qty: {item[4]} | Price: {item[6]} | Total: {item[7]}"
            )

        output_path.write_text("\n".join(lines))
        return {"message": f"Order written to {output_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Print failed: {str(e)}")

@router.post("/receive")
def receive_order(payload: dict):
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        order_id = payload.get("order_id")
        items = payload.get("items", [])

        for item in items:
            cursor.execute("""
                UPDATE order_items
                SET qty_received = ?
                WHERE order_id = ? AND item_code = ?
            """, (
                item["qty_received"],
                order_id,
                item["item_code"]
            ))

        cursor.execute("""
            SELECT qty_ordered, qty_received FROM order_items WHERE order_id = ?
        """, (order_id,))
        all_items = cursor.fetchall()
        fully_received = all(qr is not None and qr >= qo for qo, qr in all_items)

        if fully_received:
            cursor.execute("""
                UPDATE orders SET status = 'Received', received_date = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), order_id))

        conn.commit()
        conn.close()
        return {"message": "Order received", "fully_received": fully_received}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Receive failed: {e}")

@router.get("/audit/{order_id}")
def get_audit(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM audit_trail WHERE order_id = ?
                ORDER BY action_date
            """, (order_id,))
            logs = [dict(row) for row in cursor.fetchall()]
        return {"audit_trail": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit fetch failed: {e}")

@router.post("/upload_attachment")
async def upload_attachment(order_id: int = Form(...), file: UploadFile = File(...)):
    import os
    try:
        folder = Path("data/uploads")
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, file.filename, str(file_path), datetime.now().isoformat()))
            conn.commit()

        return {"message": "Attachment uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
'''

file.write_text(routes_code)
print("✅ backend/endpoints/orders.py replaced with all missing routes.")

```

### `scripts/reset_and_test.sh`
**!/usr/bin/env bash**
```python
#!/usr/bin/env bash
set -euo pipefail

# 1) Kill any Uvicorn on port 8004
if lsof -i:8004 | grep -q LISTEN; then
  echo "⏳ Stopping old server…"
  lsof -ti:8004 | xargs kill -9
  sleep 1
else
  echo "⚠ no process on port 8004"
fi

# 2) Delete the old DB
echo "🗑 Removing old database…"
rm -f data/orders.db

# 3) Recreate all tables
echo "📦 Initializing schema…"
python3 - << 'EOF'
from backend.database import init_db
init_db()
EOF

# 4) Seed lookups (requesters, suppliers, plus you can add projects/users/items here)
echo "🌱 Seeding lookup tables…"
sqlite3 data/orders.db << 'EOF'
-- requesters
INSERT OR IGNORE INTO requesters(name) VALUES
  ('Aaron'),('Leon'),('Gert'),('Omar'),('Raymond'),('Yolandi');
-- suppliers
INSERT OR IGNORE INTO suppliers(account_number,name) VALUES
  ('SUPP001','Test Supplier');
-- projects (optional stub)
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_code TEXT UNIQUE
);
INSERT OR IGNORE INTO projects(project_code) VALUES ('TEST');
-- users (optional stub)
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password_hash TEXT NOT NULL,
  rights TEXT NOT NULL
);
INSERT OR IGNORE INTO users(username,password_hash,rights) VALUES ('aaron','<hash>','Edit');
-- items (optional stub)
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_code TEXT UNIQUE,
  item_description TEXT
);
INSERT OR IGNORE INTO items(item_code,item_description) VALUES ('TEST123','Integration Widget');
EOF

# 5) Start the server in the background
echo "🚀 Starting server…"
nohup python3 scripts/start_server.py &>/dev/null &

# 6) Wait for it to spin up
sleep 3

# 7) Fire off a test order (should land as ID=1)
echo "📝 Creating a test order…"
curl -s -X POST http://localhost:8004/orders \
  -H "Content-Type: application/json" \
  -d '{
    "requester_id": 1,
    "supplier_id": 1,
    "order_note": "Shell test order",
    "supplier_note": "Test supplier",
    "items": [{
      "item_code": "TEST123",
      "item_description": "Integration Widget",
      "project": "TEST",
      "qty_ordered": 3,
      "price": 9.99
    }]
  }' | jq .

# 8) Run your validation script
echo "🔍 Running validation…"
python3 scripts/validate_repaired_routes.py

echo "✅ All done!"


```

### `scripts/seed_static_data.py`
**INSERT INTO users (username, password_hash, rights)**
```python
#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect("data/orders.db")
cursor = conn.cursor()

# --- Users ---
cursor.executemany("""
    INSERT INTO users (username, password_hash, rights)
    VALUES (?, '<hash>', ?)
""", [
    ("Aaron", "Edit"),
    ("Yolandi", "View"),
    ("Steven", "Admin"),
])

# --- Requesters ---
cursor.executemany("""
    INSERT INTO requesters (name) VALUES (?)
""", [
    ("Leon",),
    ("Aaron",),
    ("Raymond",),
    ("Yolande",),
    ("Omar",),
])

# --- Projects ---
cursor.executemany("""
    INSERT INTO projects (project_code) VALUES (?)
""", [
    ("PRO001",),
    ("PRO002",),
    ("PRO003",),
])

# --- Suppliers ---
cursor.executemany("""
    INSERT INTO suppliers (account_number, name) VALUES (?, ?)
""", [
    ("SUP001", "Supplier 1"),
    ("SUP002", "Supplier 2"),
    ("SUP003", "Supplier 3"),
])

# --- Items ---
cursor.executemany("""
    INSERT INTO items (item_code, item_description) VALUES (?, ?)
""", [
    ("ITM001", "Item 1"),
    ("ITM002", "Item 2"),
    ("ITM003", "Item 3"),
])

conn.commit()
conn.close()
print("✅ Static data inserted.")


```

### `scripts/start_server.py`
**!/usr/bin/env python3**
```python
#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

# --- CONFIG ---
PORT = "8004"
APP_MODULE = "backend.main:app"
LOG_FILE = "logs/server.log"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# --------------

print("🟢 Starting FastAPI server...")

# 1. Enforce project root and module importability
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

# 2. Kill any process using the port
print(f"🔪 Killing processes on port {PORT}...")
subprocess.run(f"lsof -ti:{PORT} | xargs kill -9", shell=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Port cleared.")

# 3. Remove all __pycache__ folders
print("🧹 Removing bytecode caches...")
for path in PROJECT_ROOT.rglob("__pycache__"):
    try:
        shutil.rmtree(path)
        print(f"   • Removed {path}")
    except Exception:
        pass

# 4. Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# 5. Start Uvicorn with reload and persistent logging
print(f"🚀 Launching Uvicorn → {APP_MODULE} on port {PORT}...")
with open(LOG_FILE, "a") as log_file:
    subprocess.Popen(
        ["venv/bin/uvicorn", APP_MODULE, "--host", "0.0.0.0", "--port", PORT, "--reload"],
        stdout=log_file,
        stderr=log_file
    )

print(f"✅ Server launched. Logs → {LOG_FILE}")

```

### `scripts/test_authorisation_threshold_trigger.py`
**(No description)**
```python
import requests
import sqlite3
from datetime import datetime

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    print(f"✅ {message}")

def fetch_one(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

def create_high_value_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "Test high value order",
        "note_to_supplier": "Handle with care",
        "items": [
            {
                "item_code": "HIGH001",
                "item_description": "Premium Machine Part",
                "project": "TestProjX",
                "qty_ordered": 1,
                "price": 20000.0  # High price to trigger threshold
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(response.status_code == 200, "Order creation succeeded")
    data = response.json()
    return data["order"]["id"], data["order"]["order_number"]

def check_authorisation_status(order_id):
    row = fetch_one("SELECT status, total FROM orders WHERE id = ?", (order_id,))
    status, total = row
    assert_condition(status == "Awaiting Authorisation", "Status is Awaiting Authorisation")
    assert_condition(total > 10000, "Total is above threshold")

def main():
    print("\n🚨 Running high-value order auth threshold test...\n")
    order_id, order_number = create_high_value_order()
    check_authorisation_status(order_id)
    print(f"\n🎯 Test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()


```

### `scripts/test_invalid_data_handling.py`
**Case 1: Empty item list**
```python
import requests
import sqlite3
from pathlib import Path

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"  # ✅ Matches project root execution context

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    print(f"✅ {message}")

def fetch_from_db(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def count_orders():
    return fetch_from_db("SELECT COUNT(*) FROM orders")[0][0]

def send_invalid_payload(payload, expected_error):
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    print(f"⚠️ Full response: {response.status_code} {response.text}")
    assert_condition(response.status_code in (400, 422), "400 or 422 received for invalid payload")
    assert_condition(expected_error.lower() in response.text.lower(), f"Error message contains '{expected_error}'")

def main():
    print("\n🧪 Testing invalid item list edge cases...\n")

    if not Path(DB_PATH).exists():
        raise FileNotFoundError(f"❌ Cannot find DB at: {DB_PATH}")

    initial_count = count_orders()

    # Case 1: Empty item list
    payload1 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": []
    }
    send_invalid_payload(payload1, "at least")  # ← fixed here

    # Case 2: Missing item_code
    payload2 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": [{
            "item_description": "Missing code",
            "project": "X",
            "qty_ordered": 1,
            "price": 10
        }]
    }
    send_invalid_payload(payload2, "item_code")

    # Case 3: Missing project
    payload3 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": [{
            "item_code": "X123",
            "item_description": "Test",
            "qty_ordered": 1,
            "price": 10
        }]
    }
    send_invalid_payload(payload3, "project")

    final_count = count_orders()
    assert_condition(final_count == initial_count, "❄️ No invalid orders inserted")

    print("\n✅ All item validation tests passed\n")

if __name__ == "__main__":
    main()

```

### `scripts/test_invalid_items_variants.py`
**Case 1: Empty item list**
```python
import requests
import sqlite3
import os

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    print(f"✅ {message}")

def fetch_from_db(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def count_orders():
    return fetch_from_db("SELECT COUNT(*) FROM orders")[0][0]

def send_invalid_payload(payload, expected_error):
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    print(f"⚠️ Full response: {response.status_code} {response.text}")
    assert_condition(response.status_code in (400, 422), "400 or 422 received for invalid payload")
    assert_condition(expected_error.lower() in response.text.lower(), f"Error message contains '{expected_error}'")

def main():
    print("\n🧪 Testing invalid item list edge cases...\n")

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"❌ Cannot find DB at: {DB_PATH}")

    initial_count = count_orders()

    # Case 1: Empty item list
    payload1 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": []
    }
    send_invalid_payload(payload1, "at least one item")

    # Case 2: Missing item_code
    payload2 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": [{
            "item_description": "Missing code",
            "project": "X",
            "qty_ordered": 1,
            "price": 10
        }]
    }
    send_invalid_payload(payload2, "item_code")

    # Case 3: Missing project
    payload3 = {
        "requester_id": 1,
        "supplier_id": 1,
        "items": [{
            "item_code": "X123",
            "item_description": "Test",
            "qty_ordered": 1,
            "price": 10
        }]
    }
    send_invalid_payload(payload3, "project")

    final_count = count_orders()
    assert_condition(final_count == initial_count, "❄️ No invalid orders inserted")

    print("\n✅ All item validation tests passed\n")

if __name__ == "__main__":
    main()


```

### `scripts/test_pipeline_end_to_end.py`
**(No description)**
```python
import requests
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"
LOG_FILE = Path("logs/testing_log.txt")

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {msg}\n")

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    log(f"✅ {message}")

def fetch_from_db(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def create_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "End-to-end test order",
        "note_to_supplier": "Please confirm ASAP",
        "items": [
            {
                "item_code": "TST001",
                "item_description": "Test Widget",
                "project": "TEST-01",
                "qty_ordered": 3,
                "price": 200.0
            },
            {
                "item_code": "TST002",
                "item_description": "Test Cable",
                "project": "TEST-02",
                "qty_ordered": 5,
                "price": 100.0
            }
        ]
    }
    res = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(res.status_code == 200, "Order creation succeeded")
    data = res.json()["order"]
    return data["id"], data["order_number"]

def get_item_ids(order_id):
    rows = fetch_from_db("SELECT id FROM order_items WHERE order_id = ?", (order_id,))
    assert_condition(len(rows) == 2, "Line items created in DB")
    return [r[0] for r in rows]

def receive_order(order_id, item_ids):
    payload = [
        {"order_id": order_id, "item_id": item_ids[0], "qty_received": 3},
        {"order_id": order_id, "item_id": item_ids[1], "qty_received": 5}
    ]
    res = requests.post(f"{BASE_URL}/orders/receive", json=payload)
    log(f"⚠️ Receive response status: {res.status_code}")
    log(f"⚠️ Response content: {res.text}")
    assert_condition(res.status_code == 200, "Order receiving succeeded")

def check_audit_trail(order_id):
    trail = fetch_from_db("SELECT action FROM audit_trail WHERE order_id = ?", (order_id,))
    assert_condition(any("Received" in row[0] for row in trail), "Audit trail entries exist")

def upload_attachment(order_id):
    dummy_file = Path("/Users/stevencohen/Desktop/test_invoice.pdf")
    if not dummy_file.exists():
        dummy_file.write_text("Dummy PDF content")

    with dummy_file.open("rb") as f:
        res = requests.post(
            f"{BASE_URL}/orders/upload_attachment",
            files={"file": f},
            data={"order_id": str(order_id)}
        )
    assert_condition(res.status_code == 200, "Attachment uploaded")

def check_attachment_record(order_id):
    rec = fetch_from_db("SELECT filename FROM attachments WHERE order_id = ?", (order_id,))
    assert_condition(len(rec) > 0, "Attachment record exists")

def main():
    LOG_FILE.write_text("🚀 Test started\n")
    log("🚀 Running full pipeline integration test...\n")
    order_id, order_number = create_order()
    item_ids = get_item_ids(order_id)
    receive_order(order_id, item_ids)
    check_audit_trail(order_id)
    upload_attachment(order_id)
    check_attachment_record(order_id)
    log(f"\n🎉 Pipeline test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()

```

### `scripts/test_receive_partial.py`
**(No description)**
```python
import requests
import sqlite3
from datetime import datetime
import os

BASE_URL = "http://localhost:8004"
DB_PATH = "data/orders.db"

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(f"❌ {message}")
    print(f"✅ {message}")

def fetch_one(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

def fetch_all(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def create_order():
    payload = {
        "requester_id": 1,
        "supplier_id": 1,
        "order_note": "Partial receive test",
        "note_to_supplier": "Split delivery test",
        "items": [
            {
                "item_code": "PART001",
                "item_description": "Partial Item A",
                "project": "SplitProjA",
                "qty_ordered": 10,
                "price": 100.0
            },
            {
                "item_code": "PART002",
                "item_description": "Partial Item B",
                "project": "SplitProjB",
                "qty_ordered": 5,
                "price": 200.0
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert_condition(response.status_code == 200, "Partial order creation succeeded")
    data = response.json()["order"]
    return data["id"], data["order_number"]

def get_item_ids(order_id):
    rows = fetch_all("SELECT id FROM order_items WHERE order_id = ?", (order_id,))
    return [r[0] for r in rows]

def receive_partial(order_id, item_ids):
    payload = [
        {"order_id": order_id, "item_id": item_ids[0], "qty_received": 10},  # full
        {"order_id": order_id, "item_id": item_ids[1], "qty_received": 2},   # partial
    ]
    response = requests.post(f"{BASE_URL}/orders/receive", json=payload)
    print("⚠️ Receive response:", response.status_code, response.text)
    assert_condition(response.status_code == 200, "Partial receipt posted")

def validate_partial(order_id):
    status, received_date = fetch_one("SELECT status, received_date FROM orders WHERE id = ?", (order_id,))
    assert_condition(status == "Pending", "Order status remains Pending")
    assert_condition(received_date is None, "No received_date set for partial receipt")

    row = fetch_one("SELECT qty_received FROM order_items WHERE order_id = ? AND qty_received < qty_ordered", (order_id,))
    assert_condition(row is not None, "At least one item is partially received")

    audit_entries = fetch_all("SELECT action, details FROM audit_trail WHERE order_id = ?", (order_id,))
    assert_condition(len(audit_entries) >= 2, "Audit entries exist for both lines")

def main():
    print("🔍 Running partial receipt test...\n")
    order_id, order_number = create_order()
    item_ids = get_item_ids(order_id)
    receive_partial(order_id, item_ids)
    validate_partial(order_id)
    print(f"\n✅ Partial receipt test passed for order {order_number} (ID {order_id})")

if __name__ == "__main__":
    main()


```

### `.git/COMMIT_EDITMSG`
**(No description)**
```python
📝 Auto-commit by script

```

### `.git/FETCH_HEAD`
**(No description)**
```python
733ef8d6650df9b401c93a63914a204045d8d2ba		branch 'main' of github.com:steven-cohen714-gmailcom/orders_project

```

### `.git/HEAD`
**(No description)**
```python
ref: refs/heads/main

```

### `.git/ORIG_HEAD`
**(No description)**
```python
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a

```

### `.git/config`
**(No description)**
```python
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
[remote "origin"]
	url = git@github.com:steven-cohen714-gmailcom/orders_project.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[pull]
	rebase = false
[branch "main"]
	remote = origin
	merge = refs/heads/main
	vscode-merge-base = origin/main
	vscode-merge-base = origin/main

```

### `.git/description`
**(No description)**
```python
Unnamed repository; edit this file 'description' to name the repository.

```

### `.git/index`
**(No description)**
```python
<!-- ERROR reading index: 'utf-8' codec can't decode byte 0xf3 in position 14: invalid continuation byte -->
```

### `.git/objects/61/1cec552867a6d50b7edd700c86c7396d906ea2`
**(No description)**
```python
<!-- ERROR reading 1cec552867a6d50b7edd700c86c7396d906ea2: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/61/339a6fcc1b82803136f3bf980e0c8f574b2220`
**(No description)**
```python
<!-- ERROR reading 339a6fcc1b82803136f3bf980e0c8f574b2220: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/61/4848e0dbaeb2cfc1356d3393b0d0992922d47f`
**(No description)**
```python
<!-- ERROR reading 4848e0dbaeb2cfc1356d3393b0d0992922d47f: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/61/502691abdcde4ce790cb16c4d28002a6241311`
**(No description)**
```python
<!-- ERROR reading 502691abdcde4ce790cb16c4d28002a6241311: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/61/54cf09431f72258638a927c1e360fd42c31ff3`
**(No description)**
```python
<!-- ERROR reading 54cf09431f72258638a927c1e360fd42c31ff3: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/61/790973cd6ed90be025982d5643d548581f4af9`
**(No description)**
```python
<!-- ERROR reading 790973cd6ed90be025982d5643d548581f4af9: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/61/8f6c25917463b0ca3c98485848d7a17794bf16`
**(No description)**
```python
<!-- ERROR reading 8f6c25917463b0ca3c98485848d7a17794bf16: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/61/d5fb6ac42ca4152f056d996af0cb0b0d2ddc35`
**(No description)**
```python
<!-- ERROR reading d5fb6ac42ca4152f056d996af0cb0b0d2ddc35: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/0d/12584b45995d35110f75af00193fdad0fa10f4`
**(No description)**
```python
<!-- ERROR reading 12584b45995d35110f75af00193fdad0fa10f4: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/0d/24def711344ec6f4da2108f7d5c9261eb35f8b`
**(No description)**
```python
<!-- ERROR reading 24def711344ec6f4da2108f7d5c9261eb35f8b: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/0d/378b66d76b8132bb8b915576c7c4257143305a`
**(No description)**
```python
<!-- ERROR reading 378b66d76b8132bb8b915576c7c4257143305a: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/0d/3b9b77e611d2d861fdaaa2940a78b03aee8a91`
**(No description)**
```python
<!-- ERROR reading 3b9b77e611d2d861fdaaa2940a78b03aee8a91: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/0d/452e27f358568a0b8d74481854bc106f5213e5`
**(No description)**
```python
<!-- ERROR reading 452e27f358568a0b8d74481854bc106f5213e5: 'utf-8' codec can't decode byte 0xcd in position 4: invalid continuation byte -->
```

### `.git/objects/0d/611859c7251858015b979e2168924cdabbc97d`
**(No description)**
```python
<!-- ERROR reading 611859c7251858015b979e2168924cdabbc97d: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/0d/6ba546ebba260296e60b8a822eed6b813770e4`
**(No description)**
```python
<!-- ERROR reading 6ba546ebba260296e60b8a822eed6b813770e4: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/0d/7cde1dfe6553960118f2581a265fa1454c3c12`
**(No description)**
```python
<!-- ERROR reading 7cde1dfe6553960118f2581a265fa1454c3c12: 'utf-8' codec can't decode byte 0xcb in position 4: invalid continuation byte -->
```

### `.git/objects/0d/8450233fbaed437174dbff6139e2cf21ab8f8c`
**(No description)**
```python
<!-- ERROR reading 8450233fbaed437174dbff6139e2cf21ab8f8c: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/0d/97560c1b791956726b04fd66740a947647aabe`
**(No description)**
```python
<!-- ERROR reading 97560c1b791956726b04fd66740a947647aabe: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/0d/b6ac5eba1152ca5c748ba1315d6ff55c3b2c71`
**(No description)**
```python
<!-- ERROR reading b6ac5eba1152ca5c748ba1315d6ff55c3b2c71: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/0d/c002edd9410b9120a518e31972b978e54b57b1`
**(No description)**
```python
<!-- ERROR reading c002edd9410b9120a518e31972b978e54b57b1: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/0d/d0914996fb742a4e7c66d9561175905587c67a`
**(No description)**
```python
<!-- ERROR reading d0914996fb742a4e7c66d9561175905587c67a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0d/dc7367cc608dac2cfb408a08c8b442278a8207`
**(No description)**
```python
<!-- ERROR reading dc7367cc608dac2cfb408a08c8b442278a8207: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/0d/e09b8d09e5347114858f1db773fabf50c6ecfe`
**(No description)**
```python
<!-- ERROR reading e09b8d09e5347114858f1db773fabf50c6ecfe: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/95/0a208a977bbf3a861bec4a01aa511848e9deb2`
**(No description)**
```python
<!-- ERROR reading 0a208a977bbf3a861bec4a01aa511848e9deb2: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/95/1549753afa255148c7c60d868303963f8c1813`
**(No description)**
```python
<!-- ERROR reading 1549753afa255148c7c60d868303963f8c1813: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/95/4ab32f234a72536fbd1655efd90adda9e6e3cf`
**(No description)**
```python
<!-- ERROR reading 4ab32f234a72536fbd1655efd90adda9e6e3cf: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/95/82fa730f121634348a79c1a8b0cc2df99c616f`
**(No description)**
```python
<!-- ERROR reading 82fa730f121634348a79c1a8b0cc2df99c616f: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/95/cf241c3e99ea2a022f388d257a83493d063284`
**(No description)**
```python
<!-- ERROR reading cf241c3e99ea2a022f388d257a83493d063284: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/95/e1869658566aac3060562d8cd5a6b647887d1e`
**(No description)**
```python
<!-- ERROR reading e1869658566aac3060562d8cd5a6b647887d1e: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/95/e9fda186fc8f5b884215f7bea251b515e72cae`
**(No description)**
```python
<!-- ERROR reading e9fda186fc8f5b884215f7bea251b515e72cae: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/59/426ef949ed9276b5708f9f44e6893f2333f2e1`
**(No description)**
```python
<!-- ERROR reading 426ef949ed9276b5708f9f44e6893f2333f2e1: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/59/460062e47950da87aa20a5f99a8993c0852022`
**(No description)**
```python
<!-- ERROR reading 460062e47950da87aa20a5f99a8993c0852022: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/59/6b516a5b6bb1134b8b24513f64c7b2f936cded`
**(No description)**
```python
<!-- ERROR reading 6b516a5b6bb1134b8b24513f64c7b2f936cded: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/59/72a96d8ded85cc14147ffc1400ec67c3b5a578`
**(No description)**
```python
<!-- ERROR reading 72a96d8ded85cc14147ffc1400ec67c3b5a578: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/59/a36799093529feaf6167b81433b56e6b8e785c`
**(No description)**
```python
<!-- ERROR reading a36799093529feaf6167b81433b56e6b8e785c: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/59/e8ef6e7427ed2f548c1da72c9acceb82ef31fa`
**(No description)**
```python
<!-- ERROR reading e8ef6e7427ed2f548c1da72c9acceb82ef31fa: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/92/069440ffa38e09cb61b3f1fd8dab6a8bd0ddf7`
**(No description)**
```python
<!-- ERROR reading 069440ffa38e09cb61b3f1fd8dab6a8bd0ddf7: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/92/3a832b2a59974d7843d6b6ef5e7fa9a83d6f71`
**(No description)**
```python
<!-- ERROR reading 3a832b2a59974d7843d6b6ef5e7fa9a83d6f71: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/92/880a49fcced8ae1fb7c8eff6bc9e7e5977cb17`
**(No description)**
```python
<!-- ERROR reading 880a49fcced8ae1fb7c8eff6bc9e7e5977cb17: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/92/ade55f7c015f4c8740cf6176e80f51f8f771ab`
**(No description)**
```python
<!-- ERROR reading ade55f7c015f4c8740cf6176e80f51f8f771ab: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/92/c4c6a193873ce09629f6cfaa2dabc4f14ecb03`
**(No description)**
```python
<!-- ERROR reading c4c6a193873ce09629f6cfaa2dabc4f14ecb03: 'utf-8' codec can't decode byte 0x93 in position 3: invalid start byte -->
```

### `.git/objects/92/cba6632f151eb91d844a1735fe1f8619e650e9`
**(No description)**
```python
<!-- ERROR reading cba6632f151eb91d844a1735fe1f8619e650e9: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/92/e302ce824c86d76ea495f09ae1b78e378b1d4e`
**(No description)**
```python
<!-- ERROR reading e302ce824c86d76ea495f09ae1b78e378b1d4e: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/92/f172bca1660978b0ab6d9abb737171856496a2`
**(No description)**
```python
<!-- ERROR reading f172bca1660978b0ab6d9abb737171856496a2: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/0c/51c846722a2f434eace7af3d04d360e40024ed`
**(No description)**
```python
<!-- ERROR reading 51c846722a2f434eace7af3d04d360e40024ed: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/0c/6ff5398d6019f275ba8ee7973bd98daa8aa88a`
**(No description)**
```python
<!-- ERROR reading 6ff5398d6019f275ba8ee7973bd98daa8aa88a: 'utf-8' codec can't decode byte 0x9e in position 9: invalid start byte -->
```

### `.git/objects/0c/7d6391438b32042e437868fc2e4aa86f60c23b`
**(No description)**
```python
<!-- ERROR reading 7d6391438b32042e437868fc2e4aa86f60c23b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0c/a96ddfb580b19413797f41e79f7abcecdd9d79`
**(No description)**
```python
<!-- ERROR reading a96ddfb580b19413797f41e79f7abcecdd9d79: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/0c/b270166211fe2b24b6ec636f632a77a5ca6b8f`
**(No description)**
```python
<!-- ERROR reading b270166211fe2b24b6ec636f632a77a5ca6b8f: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/0c/b868486edd9dda38f90c65f314597813128cf8`
**(No description)**
```python
<!-- ERROR reading b868486edd9dda38f90c65f314597813128cf8: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/0c/d789a44561ec6885a67b5cc975bdb0cf2f55c1`
**(No description)**
```python
<!-- ERROR reading d789a44561ec6885a67b5cc975bdb0cf2f55c1: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0c/e744ce80b0d943396dd460538ee3a888c6328e`
**(No description)**
```python
<!-- ERROR reading e744ce80b0d943396dd460538ee3a888c6328e: 'utf-8' codec can't decode byte 0xa9 in position 19: invalid start byte -->
```

### `.git/objects/66/33348612fa8ab9c30fb3017d5f83f336a8e1c3`
**(No description)**
```python
<!-- ERROR reading 33348612fa8ab9c30fb3017d5f83f336a8e1c3: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/66/401bdda7dc1f0b1ae8bd0f7d81b998c9cd3304`
**(No description)**
```python
<!-- ERROR reading 401bdda7dc1f0b1ae8bd0f7d81b998c9cd3304: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/66/4d1918f51e3a61b5b1dd483e63749a2af12b59`
**(No description)**
```python
<!-- ERROR reading 4d1918f51e3a61b5b1dd483e63749a2af12b59: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/66/516def9378071d2a129f4d19fbbef337905049`
**(No description)**
```python
<!-- ERROR reading 516def9378071d2a129f4d19fbbef337905049: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/66/8538695f96d7eccf8bc83f551aa5808efab1f9`
**(No description)**
```python
<!-- ERROR reading 8538695f96d7eccf8bc83f551aa5808efab1f9: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/66/a5636298f521d6f6936fcb27632f10bf76036a`
**(No description)**
```python
<!-- ERROR reading a5636298f521d6f6936fcb27632f10bf76036a: 'utf-8' codec can't decode byte 0xc9 in position 4: invalid continuation byte -->
```

### `.git/objects/66/b3cf2f5173de8303e13ca1e1ea54750ef4fdb3`
**(No description)**
```python
<!-- ERROR reading b3cf2f5173de8303e13ca1e1ea54750ef4fdb3: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/66/ebfb26bbb4999b9a5ca56216f34fa99fb9154d`
**(No description)**
```python
<!-- ERROR reading ebfb26bbb4999b9a5ca56216f34fa99fb9154d: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/66/f4fa6a47b9e6c72ae226ab9e8a88711a478d9d`
**(No description)**
```python
<!-- ERROR reading f4fa6a47b9e6c72ae226ab9e8a88711a478d9d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/66/fd99d702480b555c06694fe14715ea6df3dfc3`
**(No description)**
```python
<!-- ERROR reading fd99d702480b555c06694fe14715ea6df3dfc3: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/3e/20ef23cd81e0d4fb54898f2b642882d3d0d5ef`
**(No description)**
```python
<!-- ERROR reading 20ef23cd81e0d4fb54898f2b642882d3d0d5ef: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/3e/4c32f35acdb0aeb4448ecb4ff92193a6d4803e`
**(No description)**
```python
<!-- ERROR reading 4c32f35acdb0aeb4448ecb4ff92193a6d4803e: 'utf-8' codec can't decode byte 0xdb in position 4: invalid continuation byte -->
```

### `.git/objects/3e/5b20826ab1e354fad6ad4e1c13065866d6336f`
**(No description)**
```python
<!-- ERROR reading 5b20826ab1e354fad6ad4e1c13065866d6336f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/3e/92463e6bd522a2a21e5f0a80d8089d6c4be20d`
**(No description)**
```python
<!-- ERROR reading 92463e6bd522a2a21e5f0a80d8089d6c4be20d: 'utf-8' codec can't decode byte 0xdd in position 4: invalid continuation byte -->
```

### `.git/objects/3e/9f9f5d9fbf40b14e2cf710406ccffbc70796b5`
**(No description)**
```python
<!-- ERROR reading 9f9f5d9fbf40b14e2cf710406ccffbc70796b5: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/3e/f60ca69c41566f1b0cfda4305eaeaef9588a59`
**(No description)**
```python
<!-- ERROR reading f60ca69c41566f1b0cfda4305eaeaef9588a59: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/50/15fc97712ee08a1ec79e331922b5b0b82d0306`
**(No description)**
```python
<!-- ERROR reading 15fc97712ee08a1ec79e331922b5b0b82d0306: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/50/5164bc02d63fe6b0b3299f849a77c5f1beeb41`
**(No description)**
```python
<!-- ERROR reading 5164bc02d63fe6b0b3299f849a77c5f1beeb41: 'utf-8' codec can't decode byte 0xc1 in position 3: invalid start byte -->
```

### `.git/objects/50/70516eb56679f863bd446c97cf76376d80d83b`
**(No description)**
```python
<!-- ERROR reading 70516eb56679f863bd446c97cf76376d80d83b: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/50/ac9e2b65e0e2a8632c3c5f9532f1e17db9d380`
**(No description)**
```python
<!-- ERROR reading ac9e2b65e0e2a8632c3c5f9532f1e17db9d380: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/50/af14440d4f0fc216c9923058f1734957e08d66`
**(No description)**
```python
<!-- ERROR reading af14440d4f0fc216c9923058f1734957e08d66: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/50/d4fa5e68439ce837f6eef437b299c0dd7c8594`
**(No description)**
```python
<!-- ERROR reading d4fa5e68439ce837f6eef437b299c0dd7c8594: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/50/d7e1f11bcc7e093c75ce0563630d6caf396828`
**(No description)**
```python
<!-- ERROR reading d7e1f11bcc7e093c75ce0563630d6caf396828: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/68/38a23ecc7419f0478449d9d680c230a99c20e0`
**(No description)**
```python
<!-- ERROR reading 38a23ecc7419f0478449d9d680c230a99c20e0: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/68/82c475cacf077cf2dbb9e08a21efdab524ad16`
**(No description)**
```python
<!-- ERROR reading 82c475cacf077cf2dbb9e08a21efdab524ad16: 'utf-8' codec can't decode byte 0x8b in position 5: invalid start byte -->
```

### `.git/objects/68/9208d3c63f1318e3a9a084a90e6b4532fa49bb`
**(No description)**
```python
<!-- ERROR reading 9208d3c63f1318e3a9a084a90e6b4532fa49bb: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/68/b7f0464ece32edfb955eec0cb24655752716d6`
**(No description)**
```python
<!-- ERROR reading b7f0464ece32edfb955eec0cb24655752716d6: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/68/fba44f14366c448f13db3cf9cf1665af2e498c`
**(No description)**
```python
<!-- ERROR reading fba44f14366c448f13db3cf9cf1665af2e498c: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/57/1be44461b0847c9edb8654c9d528abed0b7800`
**(No description)**
```python
<!-- ERROR reading 1be44461b0847c9edb8654c9d528abed0b7800: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/57/8c4107f75ca3879912fcbc318ff47963d730d4`
**(No description)**
```python
<!-- ERROR reading 8c4107f75ca3879912fcbc318ff47963d730d4: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/57/8cda6f32d6d52867336075d95effb947a855b1`
**(No description)**
```python
<!-- ERROR reading 8cda6f32d6d52867336075d95effb947a855b1: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/57/dbdbdca4ed03471313a1ee729f8cc1c3f425e7`
**(No description)**
```python
<!-- ERROR reading dbdbdca4ed03471313a1ee729f8cc1c3f425e7: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/57/e2b587aae05167540abdd2b53c7b5bcac298f0`
**(No description)**
```python
<!-- ERROR reading e2b587aae05167540abdd2b53c7b5bcac298f0: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/57/e32dab1056794337fb306376b416fd1af47b20`
**(No description)**
```python
<!-- ERROR reading e32dab1056794337fb306376b416fd1af47b20: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/57/f3c211bb5121e8ad2eb814dc9f546b7fc037de`
**(No description)**
```python
<!-- ERROR reading f3c211bb5121e8ad2eb814dc9f546b7fc037de: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/3b/0e48445a8711f5c898811db9d62a34686ef18e`
**(No description)**
```python
<!-- ERROR reading 0e48445a8711f5c898811db9d62a34686ef18e: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/3b/2da0cc33e27260a3de4ba84658b82b0e105065`
**(No description)**
```python
<!-- ERROR reading 2da0cc33e27260a3de4ba84658b82b0e105065: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/3b/4d0ae4ccab143e8bde80d60967e071901c35a5`
**(No description)**
```python
<!-- ERROR reading 4d0ae4ccab143e8bde80d60967e071901c35a5: 'utf-8' codec can't decode byte 0xcc in position 3: invalid continuation byte -->
```

### `.git/objects/3b/5e64b5e6c4a210201d1676a891fd57b15cda99`
**(No description)**
```python
<!-- ERROR reading 5e64b5e6c4a210201d1676a891fd57b15cda99: 'utf-8' codec can't decode byte 0xc8 in position 3: invalid continuation byte -->
```

### `.git/objects/3b/6ec2de1c130e5539d5227b26894e10e77e6c44`
**(No description)**
```python
<!-- ERROR reading 6ec2de1c130e5539d5227b26894e10e77e6c44: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/3b/75214532281f3fb193a719125fea0455900f71`
**(No description)**
```python
<!-- ERROR reading 75214532281f3fb193a719125fea0455900f71: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/3b/bffb5d22be544df880d72db86978e84e59678c`
**(No description)**
```python
<!-- ERROR reading bffb5d22be544df880d72db86978e84e59678c: 'utf-8' codec can't decode byte 0xf1 in position 21: invalid continuation byte -->
```

### `.git/objects/3b/c77a4e23776bf3916ea2e2e138a36cd5ad73cf`
**(No description)**
```python
<!-- ERROR reading c77a4e23776bf3916ea2e2e138a36cd5ad73cf: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/3b/cd6dedd9b6e2117c2d63286ba1d1dc6cfdf510`
**(No description)**
```python
<!-- ERROR reading cd6dedd9b6e2117c2d63286ba1d1dc6cfdf510: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6f/479a0885f723b7395843d41164a87041820776`
**(No description)**
```python
<!-- ERROR reading 479a0885f723b7395843d41164a87041820776: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/6f/53f5f2a025e01e9949e2530bd9ca6928859251`
**(No description)**
```python
<!-- ERROR reading 53f5f2a025e01e9949e2530bd9ca6928859251: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6f/62d44e4ef733c0e713afcd2371fed7f2b3de67`
**(No description)**
```python
<!-- ERROR reading 62d44e4ef733c0e713afcd2371fed7f2b3de67: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/6f/d8bb6355970026602b601acd97ea520a42ea34`
**(No description)**
```python
<!-- ERROR reading d8bb6355970026602b601acd97ea520a42ea34: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/6f/ebad9ff7ff41755ed0adb048db83e598f6b56f`
**(No description)**
```python
<!-- ERROR reading ebad9ff7ff41755ed0adb048db83e598f6b56f: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/03/4fc80d20ea4a59d77af6f808dbcfc3b87612c3`
**(No description)**
```python
<!-- ERROR reading 4fc80d20ea4a59d77af6f808dbcfc3b87612c3: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/03/e4c40c4c152e4088db65090c50100368014ec4`
**(No description)**
```python
<!-- ERROR reading e4c40c4c152e4088db65090c50100368014ec4: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/03/fbdfcc944ef6f969744134957a428d19c743ca`
**(No description)**
```python
<!-- ERROR reading fbdfcc944ef6f969744134957a428d19c743ca: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/9b/6edca03d4d4b34f355fd53e49d4b4c699c972c`
**(No description)**
```python
<!-- ERROR reading 6edca03d4d4b34f355fd53e49d4b4c699c972c: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/9b/b0b18dc0d809dbc03d9ca355818b3bb0af573b`
**(No description)**
```python
<!-- ERROR reading b0b18dc0d809dbc03d9ca355818b3bb0af573b: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/9e/28b22766d8a4bd0af8949445f3f1aa2f684c6a`
**(No description)**
```python
<!-- ERROR reading 28b22766d8a4bd0af8949445f3f1aa2f684c6a: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/9e/29371678b91607a46bfe1ac2006c44df04dcc4`
**(No description)**
```python
<!-- ERROR reading 29371678b91607a46bfe1ac2006c44df04dcc4: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/9e/29623bdc54a7c6d11bcc167d71bb44cc9be39d`
**(No description)**
```python
<!-- ERROR reading 29623bdc54a7c6d11bcc167d71bb44cc9be39d: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/9e/3485e8444179d401da562e4d3c765b0abcb37c`
**(No description)**
```python
<!-- ERROR reading 3485e8444179d401da562e4d3c765b0abcb37c: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/9e/a4f1c5887c2adedcf852f3c87ff6bf695d4731`
**(No description)**
```python
<!-- ERROR reading a4f1c5887c2adedcf852f3c87ff6bf695d4731: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/9e/d2c31cba819555406044fd94e5a6788a64faad`
**(No description)**
```python
<!-- ERROR reading d2c31cba819555406044fd94e5a6788a64faad: 'utf-8' codec can't decode byte 0x88 in position 19: invalid start byte -->
```

### `.git/objects/9e/d74f37373a8fd89cb427a346d71f5b2f5f9d65`
**(No description)**
```python
<!-- ERROR reading d74f37373a8fd89cb427a346d71f5b2f5f9d65: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/9e/ddf854aaf5d2961cd55f50a531437c2668915a`
**(No description)**
```python
<!-- ERROR reading ddf854aaf5d2961cd55f50a531437c2668915a: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/9e/f1ca3686526a977d725aef8f6502e2ac5b2790`
**(No description)**
```python
<!-- ERROR reading f1ca3686526a977d725aef8f6502e2ac5b2790: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/04/30fc08bb6b256767b8511220e89ae9373fa53f`
**(No description)**
```python
<!-- ERROR reading 30fc08bb6b256767b8511220e89ae9373fa53f: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/04/512072251c429e63ed110cdbafaf4b3cca3412`
**(No description)**
```python
<!-- ERROR reading 512072251c429e63ed110cdbafaf4b3cca3412: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/04/550ac76acdd533c77d5dbccf3fd26a55a0e833`
**(No description)**
```python
<!-- ERROR reading 550ac76acdd533c77d5dbccf3fd26a55a0e833: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/04/95d10545c9fd515ed51e890309d2b66e2c30bb`
**(No description)**
```python
<!-- ERROR reading 95d10545c9fd515ed51e890309d2b66e2c30bb: 'utf-8' codec can't decode byte 0x9f in position 12: invalid start byte -->
```

### `.git/objects/04/bc00bafa2549517ec4e10e438bd3ccf1b5be5f`
**(No description)**
```python
<!-- ERROR reading bc00bafa2549517ec4e10e438bd3ccf1b5be5f: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/6a/26b0ab232e6c474dc3309a1a64bfce790e98a6`
**(No description)**
```python
<!-- ERROR reading 26b0ab232e6c474dc3309a1a64bfce790e98a6: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6a/61543342ce1dc9f0aa4f6176754a433f15bf74`
**(No description)**
```python
<!-- ERROR reading 61543342ce1dc9f0aa4f6176754a433f15bf74: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/6a/9814e5a91d64e081ecef323a761ed42d3e64de`
**(No description)**
```python
<!-- ERROR reading 9814e5a91d64e081ecef323a761ed42d3e64de: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/6a/9ff884e04880129db61e4b521be72e18c31919`
**(No description)**
```python
<!-- ERROR reading 9ff884e04880129db61e4b521be72e18c31919: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/6a/a2a7c0d00e8bcc4f2c462440380bff01e97009`
**(No description)**
```python
<!-- ERROR reading a2a7c0d00e8bcc4f2c462440380bff01e97009: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/6a/d3f466684df5c377480a8e181971a1b2f0016a`
**(No description)**
```python
<!-- ERROR reading d3f466684df5c377480a8e181971a1b2f0016a: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/6a/e9c1e69628baa2df016d4980559b60b54fe107`
**(No description)**
```python
<!-- ERROR reading e9c1e69628baa2df016d4980559b60b54fe107: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/6a/fb5c627ce3db6e61cbf46276f7ddd42552eb28`
**(No description)**
```python
<!-- ERROR reading fb5c627ce3db6e61cbf46276f7ddd42552eb28: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/32/02c70789ad37f934a67bfe19d3bc8f45efe513`
**(No description)**
```python
<!-- ERROR reading 02c70789ad37f934a67bfe19d3bc8f45efe513: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/32/05654c73b6501f1c88e69f5cd6ceb821a889c7`
**(No description)**
```python
<!-- ERROR reading 05654c73b6501f1c88e69f5cd6ceb821a889c7: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/32/0f88ed7dc296637cf9e4b1887d00b38af785f0`
**(No description)**
```python
<!-- ERROR reading 0f88ed7dc296637cf9e4b1887d00b38af785f0: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/32/37d5abf60122e0cea5463ff34f2256b11b5a81`
**(No description)**
```python
<!-- ERROR reading 37d5abf60122e0cea5463ff34f2256b11b5a81: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/32/5b8057c08cf7113d4fd889991fa5638d443793`
**(No description)**
```python
<!-- ERROR reading 5b8057c08cf7113d4fd889991fa5638d443793: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/32/8b6ecf2e5095649434da8ca93c15b77ebd278d`
**(No description)**
```python
<!-- ERROR reading 8b6ecf2e5095649434da8ca93c15b77ebd278d: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/35/3924be0e59b9ad7e6c22848c2189398481821d`
**(No description)**
```python
<!-- ERROR reading 3924be0e59b9ad7e6c22848c2189398481821d: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/35/669cc4dd809fa4007ee67c752f1be991135e77`
**(No description)**
```python
<!-- ERROR reading 669cc4dd809fa4007ee67c752f1be991135e77: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/35/93430a74f21f6e0c2faf495e1627551eebfc30`
**(No description)**
```python
<!-- ERROR reading 93430a74f21f6e0c2faf495e1627551eebfc30: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/69/261b512537f880d2bb18f9ea4b213f078f9157`
**(No description)**
```python
<!-- ERROR reading 261b512537f880d2bb18f9ea4b213f078f9157: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/69/2942ecf09bad3faf773052192ab6d470371064`
**(No description)**
```python
<!-- ERROR reading 2942ecf09bad3faf773052192ab6d470371064: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/69/2fd498e706e406658ece18ef2c8de9188c435b`
**(No description)**
```python
<!-- ERROR reading 2fd498e706e406658ece18ef2c8de9188c435b: 'utf-8' codec can't decode byte 0xcd in position 21: invalid continuation byte -->
```

### `.git/objects/69/3a45194f190ae051247e5e52516edc26bc8bf1`
**(No description)**
```python
<!-- ERROR reading 3a45194f190ae051247e5e52516edc26bc8bf1: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/69/7837bd9a87a77fc468fd1f10dd470d01701362`
**(No description)**
```python
<!-- ERROR reading 7837bd9a87a77fc468fd1f10dd470d01701362: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/69/c011ed24a32880392a842e7aa02a03d879d34d`
**(No description)**
```python
<!-- ERROR reading c011ed24a32880392a842e7aa02a03d879d34d: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/69/c8a59d3d4e038450aa37ec5b801914b817e675`
**(No description)**
```python
<!-- ERROR reading c8a59d3d4e038450aa37ec5b801914b817e675: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/69/fb6ffaff1a0716f73fea0fbce47614b84b0a77`
**(No description)**
```python
<!-- ERROR reading fb6ffaff1a0716f73fea0fbce47614b84b0a77: 'utf-8' codec can't decode byte 0xb7 in position 9: invalid start byte -->
```

### `.git/objects/3c/40bc9750e9fd11bf6ff32fa7b6f78d2476c169`
**(No description)**
```python
<!-- ERROR reading 40bc9750e9fd11bf6ff32fa7b6f78d2476c169: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/3c/50c5dcfeeda2efed282200a5c5cc8c5f7542f7`
**(No description)**
```python
<!-- ERROR reading 50c5dcfeeda2efed282200a5c5cc8c5f7542f7: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/3c/699b9a47d8628c30346fe0f9cb82dc2a4281db`
**(No description)**
```python
<!-- ERROR reading 699b9a47d8628c30346fe0f9cb82dc2a4281db: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/3c/a4eca8f295630dbb0926535b1e99900e11e788`
**(No description)**
```python
<!-- ERROR reading a4eca8f295630dbb0926535b1e99900e11e788: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte -->
```

### `.git/objects/3c/ad1486071a69c9bfe48d2834c62045ac8c1865`
**(No description)**
```python
<!-- ERROR reading ad1486071a69c9bfe48d2834c62045ac8c1865: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/56/3489e133b01e8162114e077ba9ea026dcad55b`
**(No description)**
```python
<!-- ERROR reading 3489e133b01e8162114e077ba9ea026dcad55b: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/56/5a3117b4b5e1a750bf2a4c9fdfa2d61381b0e2`
**(No description)**
```python
<!-- ERROR reading 5a3117b4b5e1a750bf2a4c9fdfa2d61381b0e2: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/56/8b7e502e9519052c8b9d89171913c76ed942af`
**(No description)**
```python
<!-- ERROR reading 8b7e502e9519052c8b9d89171913c76ed942af: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/56/9156d6ca47719f49b753a4781a86a924de173b`
**(No description)**
```python
<!-- ERROR reading 9156d6ca47719f49b753a4781a86a924de173b: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/56/b446ff987693ae3bf09601871a0ddb4c11cf62`
**(No description)**
```python
<!-- ERROR reading b446ff987693ae3bf09601871a0ddb4c11cf62: 'utf-8' codec can't decode byte 0xf5 in position 9: invalid start byte -->
```

### `.git/objects/56/cbe169d122fa42167d430b1223d2dcee906db8`
**(No description)**
```python
<!-- ERROR reading cbe169d122fa42167d430b1223d2dcee906db8: 'utf-8' codec can't decode byte 0xcb in position 4: invalid continuation byte -->
```

### `.git/objects/56/fccd9c2570d2a31365ed11278fd1b6ecc2aa54`
**(No description)**
```python
<!-- ERROR reading fccd9c2570d2a31365ed11278fd1b6ecc2aa54: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/51/3486618cd2a25a49581a3571548b2651d86412`
**(No description)**
```python
<!-- ERROR reading 3486618cd2a25a49581a3571548b2651d86412: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/51/4ff7e2e68b65f309d30a0b06e6b290d2c353a8`
**(No description)**
```python
<!-- ERROR reading 4ff7e2e68b65f309d30a0b06e6b290d2c353a8: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/51/6596c76787b10928cbab24f22c0ea00433b15d`
**(No description)**
```python
<!-- ERROR reading 6596c76787b10928cbab24f22c0ea00433b15d: 'utf-8' codec can't decode byte 0xc9 in position 3: invalid continuation byte -->
```

### `.git/objects/51/bb21dfa57dfce18515481af8df111513465b0f`
**(No description)**
```python
<!-- ERROR reading bb21dfa57dfce18515481af8df111513465b0f: 'utf-8' codec can't decode byte 0xcf in position 23: invalid continuation byte -->
```

### `.git/objects/51/bc5174628f9d172c037ed76e9f2a63e67ee92e`
**(No description)**
```python
<!-- ERROR reading bc5174628f9d172c037ed76e9f2a63e67ee92e: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/51/cacb55ca1906c731e41cab71bd1fe23b4e4ccd`
**(No description)**
```python
<!-- ERROR reading cacb55ca1906c731e41cab71bd1fe23b4e4ccd: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/51/eee1588d900f2a5ee4bf4027bb57a337f42854`
**(No description)**
```python
<!-- ERROR reading eee1588d900f2a5ee4bf4027bb57a337f42854: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/51/f3442917839f8e0f0cccb52b3c10968ad0779e`
**(No description)**
```python
<!-- ERROR reading f3442917839f8e0f0cccb52b3c10968ad0779e: 'utf-8' codec can't decode byte 0xcd in position 3: invalid continuation byte -->
```

### `.git/objects/3d/18253a741e5ec9329036907f47336a23442426`
**(No description)**
```python
<!-- ERROR reading 18253a741e5ec9329036907f47336a23442426: 'utf-8' codec can't decode byte 0xdb in position 4: invalid continuation byte -->
```

### `.git/objects/3d/20b8d02cded0aca0a8b4127b6a746e837dcb8b`
**(No description)**
```python
<!-- ERROR reading 20b8d02cded0aca0a8b4127b6a746e837dcb8b: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/3d/3b61cc9a06019489fe94bdd00c4ff904805136`
**(No description)**
```python
<!-- ERROR reading 3b61cc9a06019489fe94bdd00c4ff904805136: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/3d/5f92ebbce4da3cbde76141e902c5afb23db8db`
**(No description)**
```python
<!-- ERROR reading 5f92ebbce4da3cbde76141e902c5afb23db8db: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/3d/892992b178f1e0c418e884464b829f0d6f1779`
**(No description)**
```python
<!-- ERROR reading 892992b178f1e0c418e884464b829f0d6f1779: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/58/12cef0b5924db9af2da77f0abe4e63decee4cf`
**(No description)**
```python
<!-- ERROR reading 12cef0b5924db9af2da77f0abe4e63decee4cf: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/58/2805a0762dc7fe29c6cd910135820667ff590e`
**(No description)**
```python
<!-- ERROR reading 2805a0762dc7fe29c6cd910135820667ff590e: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/58/33d26a07d5b7c43dc79618c97c9759303a96b2`
**(No description)**
```python
<!-- ERROR reading 33d26a07d5b7c43dc79618c97c9759303a96b2: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/58/4d0ea957e117e820da9b79e9180a271189d3fc`
**(No description)**
```python
<!-- ERROR reading 4d0ea957e117e820da9b79e9180a271189d3fc: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/58/c6ca0c56bcafe43497f4a598977b27cb5e7d23`
**(No description)**
```python
<!-- ERROR reading c6ca0c56bcafe43497f4a598977b27cb5e7d23: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/67/18445290770e028ea2f1f662026c9a0b0991db`
**(No description)**
```python
<!-- ERROR reading 18445290770e028ea2f1f662026c9a0b0991db: 'utf-8' codec can't decode byte 0xbc in position 9: invalid start byte -->
```

### `.git/objects/67/486cdf427e023049eed02ed1cf85b04b1963c7`
**(No description)**
```python
<!-- ERROR reading 486cdf427e023049eed02ed1cf85b04b1963c7: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/67/561419747de2e24f9560cb4d6a53d8ad7bda5e`
**(No description)**
```python
<!-- ERROR reading 561419747de2e24f9560cb4d6a53d8ad7bda5e: 'utf-8' codec can't decode byte 0x94 in position 3: invalid start byte -->
```

### `.git/objects/67/5e6bf3743f3d3011c238657e7128ee9960ef7f`
**(No description)**
```python
<!-- ERROR reading 5e6bf3743f3d3011c238657e7128ee9960ef7f: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/67/ce2444ea69a0bbdfab0bda8c2aa14951187096`
**(No description)**
```python
<!-- ERROR reading ce2444ea69a0bbdfab0bda8c2aa14951187096: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/67/d74bf86bfc80e22d9a4a3153572845accd9039`
**(No description)**
```python
<!-- ERROR reading d74bf86bfc80e22d9a4a3153572845accd9039: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0b/3d9f51b90a0e0abd730b2601480047f520e7b6`
**(No description)**
```python
<!-- ERROR reading 3d9f51b90a0e0abd730b2601480047f520e7b6: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/0b/60301bf5f4b6369cc0991624a2a939b55fc9e5`
**(No description)**
```python
<!-- ERROR reading 60301bf5f4b6369cc0991624a2a939b55fc9e5: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/0b/7653f5825979edcd446d698d320bdb980b8e9e`
**(No description)**
```python
<!-- ERROR reading 7653f5825979edcd446d698d320bdb980b8e9e: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/0b/76dd152c6b24e553cc535431a22970947200c0`
**(No description)**
```python
<!-- ERROR reading 76dd152c6b24e553cc535431a22970947200c0: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/0b/8315166ea2594f89b18e8d6dbdff2929b3ae18`
**(No description)**
```python
<!-- ERROR reading 8315166ea2594f89b18e8d6dbdff2929b3ae18: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/0b/da22d02ffc59f306ded475805343aef2855f49`
**(No description)**
```python
<!-- ERROR reading da22d02ffc59f306ded475805343aef2855f49: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/0b/e811af2c29e5ef697b63f329b882694c91c88d`
**(No description)**
```python
<!-- ERROR reading e811af2c29e5ef697b63f329b882694c91c88d: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/0b/fa94eacb6ae5cfacf395f13511413dd6f18ad4`
**(No description)**
```python
<!-- ERROR reading fa94eacb6ae5cfacf395f13511413dd6f18ad4: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0b/fde42604dad17f9dcbfa41a63c4949cdeb962a`
**(No description)**
```python
<!-- ERROR reading fde42604dad17f9dcbfa41a63c4949cdeb962a: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/0b/fe2fffb36ebb294171bef5bc37be431b3c3156`
**(No description)**
```python
<!-- ERROR reading fe2fffb36ebb294171bef5bc37be431b3c3156: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/93/3587fba22290d7eb7df4c88e12f1e61702b8ce`
**(No description)**
```python
<!-- ERROR reading 3587fba22290d7eb7df4c88e12f1e61702b8ce: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/93/409dfea980b0baef84ad1fc3c4d7c3193d6ba0`
**(No description)**
```python
<!-- ERROR reading 409dfea980b0baef84ad1fc3c4d7c3193d6ba0: 'utf-8' codec can't decode byte 0xc7 in position 7: invalid continuation byte -->
```

### `.git/objects/93/9cdb912a9debaea07fbf3a9ac04549c44d077c`
**(No description)**
```python
<!-- ERROR reading 9cdb912a9debaea07fbf3a9ac04549c44d077c: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/93/abad38f434d7ecf8d208cdefc310bd73a5a673`
**(No description)**
```python
<!-- ERROR reading abad38f434d7ecf8d208cdefc310bd73a5a673: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/93/d1568bd4d5d63281b798b09cedbafdfaa158ee`
**(No description)**
```python
<!-- ERROR reading d1568bd4d5d63281b798b09cedbafdfaa158ee: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/94/66bf6320157d79e69d6940e2b09fb08f64da51`
**(No description)**
```python
<!-- ERROR reading 66bf6320157d79e69d6940e2b09fb08f64da51: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/94/7cd76a99e5fdde049b2b6b713ba273ea4309d5`
**(No description)**
```python
<!-- ERROR reading 7cd76a99e5fdde049b2b6b713ba273ea4309d5: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/94/95a1df1e6e8a738a6f26efed3657f2b709a11f`
**(No description)**
```python
<!-- ERROR reading 95a1df1e6e8a738a6f26efed3657f2b709a11f: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/94/e07732d91fdf38f4559da04db4221d26553d40`
**(No description)**
```python
<!-- ERROR reading e07732d91fdf38f4559da04db4221d26553d40: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/0e/02bc7a5b1748c86b414bdd019e607d5857ce07`
**(No description)**
```python
<!-- ERROR reading 02bc7a5b1748c86b414bdd019e607d5857ce07: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/0e/1658fa5e5e498bcfa84702ed1a53dfcec071ff`
**(No description)**
```python
<!-- ERROR reading 1658fa5e5e498bcfa84702ed1a53dfcec071ff: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/0e/2045b2483704453bac25999e141b935d74fd83`
**(No description)**
```python
<!-- ERROR reading 2045b2483704453bac25999e141b935d74fd83: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/0e/2fd1eb05efc526f660bcf10e865d2fe781a239`
**(No description)**
```python
<!-- ERROR reading 2fd1eb05efc526f660bcf10e865d2fe781a239: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/0e/31221543adcd5cbec489985bbf473dcf7503f6`
**(No description)**
```python
<!-- ERROR reading 31221543adcd5cbec489985bbf473dcf7503f6: 'utf-8' codec can't decode byte 0x8b in position 5: invalid start byte -->
```

### `.git/objects/0e/6035d5302016960ef42d09ded06b2338bd6c01`
**(No description)**
```python
<!-- ERROR reading 6035d5302016960ef42d09ded06b2338bd6c01: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/0e/89e64d3ea50e0f102241889e7579868978e1f3`
**(No description)**
```python
<!-- ERROR reading 89e64d3ea50e0f102241889e7579868978e1f3: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/0e/9ddaa21419e9581392d170a51dfcf53203d5e8`
**(No description)**
```python
<!-- ERROR reading 9ddaa21419e9581392d170a51dfcf53203d5e8: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/0e/b1b9c254b174e9e3be7e3322e2fcb21ea8e3aa`
**(No description)**
```python
<!-- ERROR reading b1b9c254b174e9e3be7e3322e2fcb21ea8e3aa: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/0e/d97b6443fbcf4ac1e7a6e5d46ce6d11517aba7`
**(No description)**
```python
<!-- ERROR reading d97b6443fbcf4ac1e7a6e5d46ce6d11517aba7: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/60/0b8436d7c1e833cb3c5efea898b42d15d920c0`
**(No description)**
```python
<!-- ERROR reading 0b8436d7c1e833cb3c5efea898b42d15d920c0: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/60/39a0543204739849335ad27894cf64224ad828`
**(No description)**
```python
<!-- ERROR reading 39a0543204739849335ad27894cf64224ad828: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/60/4aff8ba19599e9e88d9315ee874b35a8d4493d`
**(No description)**
```python
<!-- ERROR reading 4aff8ba19599e9e88d9315ee874b35a8d4493d: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/60/7b9452428f4343a1a017dfd230b12456060543`
**(No description)**
```python
<!-- ERROR reading 7b9452428f4343a1a017dfd230b12456060543: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/34/13149834c721ed511b1b8e64fcb248b18a8bf8`
**(No description)**
```python
<!-- ERROR reading 13149834c721ed511b1b8e64fcb248b18a8bf8: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/34/273779d77666f5cd775f6a2684641092db67ee`
**(No description)**
```python
<!-- ERROR reading 273779d77666f5cd775f6a2684641092db67ee: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/34/28a19cf197fd819e66f717d41251f8849b0da7`
**(No description)**
```python
<!-- ERROR reading 28a19cf197fd819e66f717d41251f8849b0da7: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/34/3547a4d316e48144ba6bdf342dcc24cd6cb6cd`
**(No description)**
```python
<!-- ERROR reading 3547a4d316e48144ba6bdf342dcc24cd6cb6cd: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/34/5a060d0230ada58f769b0f6b55f43a428fc3bd`
**(No description)**
```python
<!-- ERROR reading 5a060d0230ada58f769b0f6b55f43a428fc3bd: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/34/6a851da87ce5facc2bd72c68fd2d0183aa379a`
**(No description)**
```python
<!-- ERROR reading 6a851da87ce5facc2bd72c68fd2d0183aa379a: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/34/78c34c47d167f706a1f54427e3b6dece62b38f`
**(No description)**
```python
<!-- ERROR reading 78c34c47d167f706a1f54427e3b6dece62b38f: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/34/cb96fb7c876acd4826323d16ee0931636fed17`
**(No description)**
```python
<!-- ERROR reading cb96fb7c876acd4826323d16ee0931636fed17: 'utf-8' codec can't decode byte 0xd7 in position 4: invalid continuation byte -->
```

### `.git/objects/34/f884d5b314dbb28abd2af3ce159630f6028180`
**(No description)**
```python
<!-- ERROR reading f884d5b314dbb28abd2af3ce159630f6028180: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/5a/838de4f73f73a5bad2da9bb60466a6c2cf1f28`
**(No description)**
```python
<!-- ERROR reading 838de4f73f73a5bad2da9bb60466a6c2cf1f28: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/5a/8d138372de7911ad5cafc2a71c5f775e191aef`
**(No description)**
```python
<!-- ERROR reading 8d138372de7911ad5cafc2a71c5f775e191aef: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/5a/a6160b469d6e9c5b630f11c2abe211c9547281`
**(No description)**
```python
<!-- ERROR reading a6160b469d6e9c5b630f11c2abe211c9547281: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/5a/d7faef2ec69eaa737a58d3587770a612a510d8`
**(No description)**
```python
<!-- ERROR reading d7faef2ec69eaa737a58d3587770a612a510d8: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/5a/ec59827d48ac0244ceb39e85f742ad1348c203`
**(No description)**
```python
<!-- ERROR reading ec59827d48ac0244ceb39e85f742ad1348c203: 'utf-8' codec can't decode byte 0xcb in position 4: invalid continuation byte -->
```

### `.git/objects/5f/00253e2f67b6f438451bb907480d06ec6c094e`
**(No description)**
```python
<!-- ERROR reading 00253e2f67b6f438451bb907480d06ec6c094e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/5f/1cd7c47829ce17dbcf651ab56b4ffdce04a485`
**(No description)**
```python
<!-- ERROR reading 1cd7c47829ce17dbcf651ab56b4ffdce04a485: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/5f/40996a67efe9e38a6b68242efc2f10fc89e471`
**(No description)**
```python
<!-- ERROR reading 40996a67efe9e38a6b68242efc2f10fc89e471: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/5f/568f439c5868142fbc5443e509ce6ebe84f8c2`
**(No description)**
```python
<!-- ERROR reading 568f439c5868142fbc5443e509ce6ebe84f8c2: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/5f/6f217500d8ca1e7717f59ae372ee9a27660fe3`
**(No description)**
```python
<!-- ERROR reading 6f217500d8ca1e7717f59ae372ee9a27660fe3: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/5f/7d6f8a02f0293e90719bcf3c2999d8bde12c6b`
**(No description)**
```python
<!-- ERROR reading 7d6f8a02f0293e90719bcf3c2999d8bde12c6b: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/5f/9fcd883b69fb960b067f316d49401aba425b4c`
**(No description)**
```python
<!-- ERROR reading 9fcd883b69fb960b067f316d49401aba425b4c: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/5f/b609bd35a1b735128d1105656d36b7b518b7f7`
**(No description)**
```python
<!-- ERROR reading b609bd35a1b735128d1105656d36b7b518b7f7: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/5f/cdbf73f9410cb873e9410581b0ef7ac5d9ac3d`
**(No description)**
```python
<!-- ERROR reading cdbf73f9410cb873e9410581b0ef7ac5d9ac3d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/5f/fad59862ba942a26dc27ce77c66578659918d3`
**(No description)**
```python
<!-- ERROR reading fad59862ba942a26dc27ce77c66578659918d3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/33/00fdd367fa03c59347cb120dee668a9ecb2baa`
**(No description)**
```python
<!-- ERROR reading 00fdd367fa03c59347cb120dee668a9ecb2baa: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/33/0c51a5dde15a0bb610a48cd0ca11770c914dae`
**(No description)**
```python
<!-- ERROR reading 0c51a5dde15a0bb610a48cd0ca11770c914dae: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/33/349a38d69c2c14b48b0302e004a6ba08c0d07d`
**(No description)**
```python
<!-- ERROR reading 349a38d69c2c14b48b0302e004a6ba08c0d07d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/33/402333f48a8e898c5bbf593700b330c52671e3`
**(No description)**
```python
<!-- ERROR reading 402333f48a8e898c5bbf593700b330c52671e3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/33/a3b77410c02af114b01dd74b5de09f9e30562e`
**(No description)**
```python
<!-- ERROR reading a3b77410c02af114b01dd74b5de09f9e30562e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/33/a88b4aad9d756d1fe0f718260da58f45d5d342`
**(No description)**
```python
<!-- ERROR reading a88b4aad9d756d1fe0f718260da58f45d5d342: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/33/b5aed0a322d9dfdf35daffeb293bc56ff39c54`
**(No description)**
```python
<!-- ERROR reading b5aed0a322d9dfdf35daffeb293bc56ff39c54: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/33/e152cc8d178486ef016285855495a86d5991d8`
**(No description)**
```python
<!-- ERROR reading e152cc8d178486ef016285855495a86d5991d8: 'utf-8' codec can't decode byte 0xcb in position 4: invalid continuation byte -->
```

### `.git/objects/05/19ecba6ea913e21689ec692e81e9e4973fbf73`
**(No description)**
```python
<!-- ERROR reading 19ecba6ea913e21689ec692e81e9e4973fbf73: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/05/4bcddaa57adbd848f475b9e85513ba927069a1`
**(No description)**
```python
<!-- ERROR reading 4bcddaa57adbd848f475b9e85513ba927069a1: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/05/5590b98e8b1ff6251237c580212f391a7ed6fa`
**(No description)**
```python
<!-- ERROR reading 5590b98e8b1ff6251237c580212f391a7ed6fa: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/05/5a8ac1b1d21ed8d6d8c9a1217e79df9d1396c1`
**(No description)**
```python
<!-- ERROR reading 5a8ac1b1d21ed8d6d8c9a1217e79df9d1396c1: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/05/6de65424756b2be1eb28a23e447f007227bab7`
**(No description)**
```python
<!-- ERROR reading 6de65424756b2be1eb28a23e447f007227bab7: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/05/a37751f3aaf5405674269a8beec6f468f36c65`
**(No description)**
```python
<!-- ERROR reading a37751f3aaf5405674269a8beec6f468f36c65: 'utf-8' codec can't decode byte 0x9e in position 9: invalid start byte -->
```

### `.git/objects/9d/630f491d9a39644ae65564dac88eb51f0bbe78`
**(No description)**
```python
<!-- ERROR reading 630f491d9a39644ae65564dac88eb51f0bbe78: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/9d/6f0bc0dd674e92a985a5f997b17039ade95217`
**(No description)**
```python
<!-- ERROR reading 6f0bc0dd674e92a985a5f997b17039ade95217: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/9d/87e1dbd152aef15bf108eebdd4764e2f9e6850`
**(No description)**
```python
<!-- ERROR reading 87e1dbd152aef15bf108eebdd4764e2f9e6850: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/9d/fb2f24b52e4d4a806b26fe99ad9a316fcc5631`
**(No description)**
```python
<!-- ERROR reading fb2f24b52e4d4a806b26fe99ad9a316fcc5631: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/9c/3ae630da0f5fa7185edeb5c45a2df4a75b0f5d`
**(No description)**
```python
<!-- ERROR reading 3ae630da0f5fa7185edeb5c45a2df4a75b0f5d: 'utf-8' codec can't decode byte 0xc1 in position 3: invalid start byte -->
```

### `.git/objects/9c/cfa53e597a29ee387f9d16f3af4f695ac0d33a`
**(No description)**
```python
<!-- ERROR reading cfa53e597a29ee387f9d16f3af4f695ac0d33a: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/9c/d8eb06277f449599a7b4babe74e1adab33bdc2`
**(No description)**
```python
<!-- ERROR reading d8eb06277f449599a7b4babe74e1adab33bdc2: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/9c/e54ac874ea8cce752e58b9a5c6fe47d76c58cf`
**(No description)**
```python
<!-- ERROR reading e54ac874ea8cce752e58b9a5c6fe47d76c58cf: 'utf-8' codec can't decode byte 0x8d in position 22: invalid start byte -->
```

### `.git/objects/9c/e7888ef28598e083e9dad401e20a7c3f2cf145`
**(No description)**
```python
<!-- ERROR reading e7888ef28598e083e9dad401e20a7c3f2cf145: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/02/08fdf33b640cd9791359d74673bb90cfb87f96`
**(No description)**
```python
<!-- ERROR reading 08fdf33b640cd9791359d74673bb90cfb87f96: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/02/46568bd05013ed797e0514181aa43bdc59c63e`
**(No description)**
```python
<!-- ERROR reading 46568bd05013ed797e0514181aa43bdc59c63e: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/02/543fd1370844a58f51c9be0341310a515a8ef6`
**(No description)**
```python
<!-- ERROR reading 543fd1370844a58f51c9be0341310a515a8ef6: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/02/5a90351e39a0e200c1416ea12f19f006f4e922`
**(No description)**
```python
<!-- ERROR reading 5a90351e39a0e200c1416ea12f19f006f4e922: 'utf-8' codec can't decode byte 0xc8 in position 17: invalid continuation byte -->
```

### `.git/objects/02/77ea3fdd31c956a46d2a74a54c62c114647bd3`
**(No description)**
```python
<!-- ERROR reading 77ea3fdd31c956a46d2a74a54c62c114647bd3: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/02/945a947527a9bfb396d0cd35ffee22eda665bb`
**(No description)**
```python
<!-- ERROR reading 945a947527a9bfb396d0cd35ffee22eda665bb: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/02/da0777a392d1d94c27138eb58ceb1158644915`
**(No description)**
```python
<!-- ERROR reading da0777a392d1d94c27138eb58ceb1158644915: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/02/f455d8eefd53ef88da5424315589610bf7edd7`
**(No description)**
```python
<!-- ERROR reading f455d8eefd53ef88da5424315589610bf7edd7: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/a4/0eeafcc914108ca79c5d83d6e81da1b29c6e80`
**(No description)**
```python
<!-- ERROR reading 0eeafcc914108ca79c5d83d6e81da1b29c6e80: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/a4/2428388b1139df995c91eaa6609887a9b9bc8f`
**(No description)**
```python
<!-- ERROR reading 2428388b1139df995c91eaa6609887a9b9bc8f: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/a4/57f24f4df680961fffa645a70504837b6abe78`
**(No description)**
```python
<!-- ERROR reading 57f24f4df680961fffa645a70504837b6abe78: 'utf-8' codec can't decode byte 0xd0 in position 17: invalid continuation byte -->
```

### `.git/objects/a4/57ff27ef0f766ed6f9bd19858ac1ecb2f109cf`
**(No description)**
```python
<!-- ERROR reading 57ff27ef0f766ed6f9bd19858ac1ecb2f109cf: 'utf-8' codec can't decode byte 0xeb in position 4: invalid continuation byte -->
```

### `.git/objects/a4/698ec1ddacd998954ebb80d8069984acd46fe7`
**(No description)**
```python
<!-- ERROR reading 698ec1ddacd998954ebb80d8069984acd46fe7: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/a4/85c59979cb7db03d68b93be81a29f4be8327f3`
**(No description)**
```python
<!-- ERROR reading 85c59979cb7db03d68b93be81a29f4be8327f3: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/a4/a7acea822d43ba91183cff0b44f31313171d1a`
**(No description)**
```python
<!-- ERROR reading a7acea822d43ba91183cff0b44f31313171d1a: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/a4/f942c5ae3739c590d33a58453a79329d140fb1`
**(No description)**
```python
<!-- ERROR reading f942c5ae3739c590d33a58453a79329d140fb1: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/a3/23e2e567f23d333684306a59edf463de63114d`
**(No description)**
```python
<!-- ERROR reading 23e2e567f23d333684306a59edf463de63114d: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/a3/245a61afd0f59143f38ee809ee2d784d9198eb`
**(No description)**
```python
<!-- ERROR reading 245a61afd0f59143f38ee809ee2d784d9198eb: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/a3/db8794c2395b7a424c75f6bbfd86436e49d572`
**(No description)**
```python
<!-- ERROR reading db8794c2395b7a424c75f6bbfd86436e49d572: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/a3/dd8bec1fcbce0dfd924d2d0e725a1ddee2f005`
**(No description)**
```python
<!-- ERROR reading dd8bec1fcbce0dfd924d2d0e725a1ddee2f005: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b5/02fe4efd22f26e6c8fa5805e5fc06dfe82b062`
**(No description)**
```python
<!-- ERROR reading 02fe4efd22f26e6c8fa5805e5fc06dfe82b062: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/b5/1bde91b2e5b4e557ed9b70fc113843cc3d49ae`
**(No description)**
```python
<!-- ERROR reading 1bde91b2e5b4e557ed9b70fc113843cc3d49ae: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b5/48e8b8045326555222a03900f5e20f99537810`
**(No description)**
```python
<!-- ERROR reading 48e8b8045326555222a03900f5e20f99537810: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/b5/6c35a4142be76ddd2cd06f350f65cf19433e8a`
**(No description)**
```python
<!-- ERROR reading 6c35a4142be76ddd2cd06f350f65cf19433e8a: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/b5/ac1070294b478b7cc2ce677207ee08813bfa37`
**(No description)**
```python
<!-- ERROR reading ac1070294b478b7cc2ce677207ee08813bfa37: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b5/c4fd6060b42e1b552ef4ab117e313e0d6477fc`
**(No description)**
```python
<!-- ERROR reading c4fd6060b42e1b552ef4ab117e313e0d6477fc: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b5/eafda98ea65bb7c36f7f928b6cbc2c973a7264`
**(No description)**
```python
<!-- ERROR reading eafda98ea65bb7c36f7f928b6cbc2c973a7264: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/b5/f70325c4d2dd32d430d24da50c9dcebb66befa`
**(No description)**
```python
<!-- ERROR reading f70325c4d2dd32d430d24da50c9dcebb66befa: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b2/31a82e1969822695bb3680217b66e73c81d017`
**(No description)**
```python
<!-- ERROR reading 31a82e1969822695bb3680217b66e73c81d017: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/b2/3c7f69e2dfd944b79c3342c030d60561e5063f`
**(No description)**
```python
<!-- ERROR reading 3c7f69e2dfd944b79c3342c030d60561e5063f: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/b2/684ce6511f0e23da1bf16261fe2c345ed2a3e8`
**(No description)**
```python
<!-- ERROR reading 684ce6511f0e23da1bf16261fe2c345ed2a3e8: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/b2/913a4d84a0215facc3e132759ccbaef2c69588`
**(No description)**
```python
<!-- ERROR reading 913a4d84a0215facc3e132759ccbaef2c69588: 'utf-8' codec can't decode byte 0xb1 in position 8: invalid start byte -->
```

### `.git/objects/b2/b20ffcce51ff24a31083087e6a68c6b8fcc9e4`
**(No description)**
```python
<!-- ERROR reading b20ffcce51ff24a31083087e6a68c6b8fcc9e4: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/b2/d3aac3137f5d374ec35dd4bbfdb5e732fc51f0`
**(No description)**
```python
<!-- ERROR reading d3aac3137f5d374ec35dd4bbfdb5e732fc51f0: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/d9/164d6883d2dd47cb766b483592ca3730f6f09d`
**(No description)**
```python
<!-- ERROR reading 164d6883d2dd47cb766b483592ca3730f6f09d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d9/1e834bebf6b33871f3030ce35904cba271193a`
**(No description)**
```python
<!-- ERROR reading 1e834bebf6b33871f3030ce35904cba271193a: 'utf-8' codec can't decode byte 0xab in position 6: invalid start byte -->
```

### `.git/objects/d9/49412e03b29d70592c7721fe747e5085c2e280`
**(No description)**
```python
<!-- ERROR reading 49412e03b29d70592c7721fe747e5085c2e280: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/d9/55ca4771bb2cd78a8e9334a6917f9f6cce59b1`
**(No description)**
```python
<!-- ERROR reading 55ca4771bb2cd78a8e9334a6917f9f6cce59b1: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/d9/648a3661c36b0b21b1253af9f523e62446284e`
**(No description)**
```python
<!-- ERROR reading 648a3661c36b0b21b1253af9f523e62446284e: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/d9/80cd6f83e9fe3e65850c6c9c818cd70952180d`
**(No description)**
```python
<!-- ERROR reading 80cd6f83e9fe3e65850c6c9c818cd70952180d: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/d9/8bbea52e19adb95bf605672660072d09afea1e`
**(No description)**
```python
<!-- ERROR reading 8bbea52e19adb95bf605672660072d09afea1e: 'utf-8' codec can't decode byte 0xb1 in position 8: invalid start byte -->
```

### `.git/objects/d9/9323a9965f146d5b0888c4ca1bf0727e12b04f`
**(No description)**
```python
<!-- ERROR reading 9323a9965f146d5b0888c4ca1bf0727e12b04f: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/d9/9528ede7357a287df5f03236f9f7e391f6f35a`
**(No description)**
```python
<!-- ERROR reading 9528ede7357a287df5f03236f9f7e391f6f35a: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/d9/95fff0492930a50f6380b5c03f7f124064c804`
**(No description)**
```python
<!-- ERROR reading 95fff0492930a50f6380b5c03f7f124064c804: 'utf-8' codec can't decode byte 0xb3 in position 9: invalid start byte -->
```

### `.git/objects/d9/b9c017bc291f6f1840b0fe8f2982f41e31e8ea`
**(No description)**
```python
<!-- ERROR reading b9c017bc291f6f1840b0fe8f2982f41e31e8ea: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/d9/dcc2d7df8563dca3da82a069f80bebc64fbbda`
**(No description)**
```python
<!-- ERROR reading dcc2d7df8563dca3da82a069f80bebc64fbbda: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/d9/eaaafd5b6b2617baf3b3c889659c5bac807ff2`
**(No description)**
```python
<!-- ERROR reading eaaafd5b6b2617baf3b3c889659c5bac807ff2: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ac/2273701b5a0ae7cb0d0171cd08a7bbf77a9178`
**(No description)**
```python
<!-- ERROR reading 2273701b5a0ae7cb0d0171cd08a7bbf77a9178: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/ac/723703336ce7f1b74497514e3e60e63ca7e126`
**(No description)**
```python
<!-- ERROR reading 723703336ce7f1b74497514e3e60e63ca7e126: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/ac/d6c5bdd63f413208cc6c989d3cc78924d27c81`
**(No description)**
```python
<!-- ERROR reading d6c5bdd63f413208cc6c989d3cc78924d27c81: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/ac/e2237639e17b84b79f57745d9b9b048d095942`
**(No description)**
```python
<!-- ERROR reading e2237639e17b84b79f57745d9b9b048d095942: 'utf-8' codec can't decode byte 0xf1 in position 21: invalid continuation byte -->
```

### `.git/objects/ac/f94ac32d9a9d8e79d6ad1154d32675229ce6e0`
**(No description)**
```python
<!-- ERROR reading f94ac32d9a9d8e79d6ad1154d32675229ce6e0: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ad/3361ad46a29a982c4d6b9a19679f88cce082d3`
**(No description)**
```python
<!-- ERROR reading 3361ad46a29a982c4d6b9a19679f88cce082d3: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/ad/386e4f16bbe0a4ef36489e2cc61f26fb6ee73e`
**(No description)**
```python
<!-- ERROR reading 386e4f16bbe0a4ef36489e2cc61f26fb6ee73e: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/ad/7b3f3baa1be16b164e4b0ca7c37a395ef670d0`
**(No description)**
```python
<!-- ERROR reading 7b3f3baa1be16b164e4b0ca7c37a395ef670d0: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ad/92864c0f5ba6c79d5722f53b02f0932116d531`
**(No description)**
```python
<!-- ERROR reading 92864c0f5ba6c79d5722f53b02f0932116d531: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/ad/9f8f6c935568bbea49d73747dda687c6f4da5e`
**(No description)**
```python
<!-- ERROR reading 9f8f6c935568bbea49d73747dda687c6f4da5e: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ad/a250064678ee3ddfbc29244a45ca64d527659c`
**(No description)**
```python
<!-- ERROR reading a250064678ee3ddfbc29244a45ca64d527659c: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ad/b74c4cafb5dac776871681fd3fc24687b76ef1`
**(No description)**
```python
<!-- ERROR reading b74c4cafb5dac776871681fd3fc24687b76ef1: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/ad/d7df0c210f95af8310250d3ce7820aaeb170e3`
**(No description)**
```python
<!-- ERROR reading d7df0c210f95af8310250d3ce7820aaeb170e3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/bb/48ae1221beb1d8b41781b31aae19ec2e769749`
**(No description)**
```python
<!-- ERROR reading 48ae1221beb1d8b41781b31aae19ec2e769749: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/bb/5c7df181e6fe406dff36d601178188d19a18d6`
**(No description)**
```python
<!-- ERROR reading 5c7df181e6fe406dff36d601178188d19a18d6: 'utf-8' codec can't decode byte 0x85 in position 14: invalid start byte -->
```

### `.git/objects/bb/c5cda6441fc696beea666edd8ad6818ef7ea95`
**(No description)**
```python
<!-- ERROR reading c5cda6441fc696beea666edd8ad6818ef7ea95: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/bb/eb2cc7861a735d6cd5c0e29aeb6dbf8457023a`
**(No description)**
```python
<!-- ERROR reading eb2cc7861a735d6cd5c0e29aeb6dbf8457023a: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/d7/24ee3cfdbcda1c39f39511046c7a884186ca98`
**(No description)**
```python
<!-- ERROR reading 24ee3cfdbcda1c39f39511046c7a884186ca98: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/d7/257ae6bf4ed2ee1f0577fd416632d59f2bed54`
**(No description)**
```python
<!-- ERROR reading 257ae6bf4ed2ee1f0577fd416632d59f2bed54: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/d7/4f5e4e92f3edeb5a2868ac049973eef7b245cb`
**(No description)**
```python
<!-- ERROR reading 4f5e4e92f3edeb5a2868ac049973eef7b245cb: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/d7/9f73c574ffc759ef5d2145b1ec742d85c2500b`
**(No description)**
```python
<!-- ERROR reading 9f73c574ffc759ef5d2145b1ec742d85c2500b: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/d7/c2dbd266660ab3d19a66c17e33bae629f8c499`
**(No description)**
```python
<!-- ERROR reading c2dbd266660ab3d19a66c17e33bae629f8c499: 'utf-8' codec can't decode byte 0xf1 in position 22: invalid continuation byte -->
```

### `.git/objects/d7/c4926afce32cad6a36379f6e159e7fe6215c75`
**(No description)**
```python
<!-- ERROR reading c4926afce32cad6a36379f6e159e7fe6215c75: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/d0/1f925cca20f98c93e141f5954295c59b2fba03`
**(No description)**
```python
<!-- ERROR reading 1f925cca20f98c93e141f5954295c59b2fba03: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/d0/593218fd002acae235f244ef1c61b9d99ea1b8`
**(No description)**
```python
<!-- ERROR reading 593218fd002acae235f244ef1c61b9d99ea1b8: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/d0/6784f3d254176d1bd125cfd4d3af7f13005387`
**(No description)**
```python
<!-- ERROR reading 6784f3d254176d1bd125cfd4d3af7f13005387: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d0/6c77f5efbafcf93187beab7dc3f7f9d2cf7b17`
**(No description)**
```python
<!-- ERROR reading 6c77f5efbafcf93187beab7dc3f7f9d2cf7b17: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/d0/748ec419c2386e0f22c7848474f6b5e9a324b7`
**(No description)**
```python
<!-- ERROR reading 748ec419c2386e0f22c7848474f6b5e9a324b7: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d0/be0a6c5d6c19a35f0e815b83e27f8d833ea88b`
**(No description)**
```python
<!-- ERROR reading be0a6c5d6c19a35f0e815b83e27f8d833ea88b: 'utf-8' codec can't decode byte 0xc1 in position 3: invalid start byte -->
```

### `.git/objects/d0/cb5d3d4616f938aea2aae42985b4c166b500cc`
**(No description)**
```python
<!-- ERROR reading cb5d3d4616f938aea2aae42985b4c166b500cc: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/d0/f51bfa7dd15870a2b2442b491b91fefadfe29d`
**(No description)**
```python
<!-- ERROR reading f51bfa7dd15870a2b2442b491b91fefadfe29d: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/d0/f5b424890c2e6f2eb8d02cbdf9b54c6ecd8d9d`
**(No description)**
```python
<!-- ERROR reading f5b424890c2e6f2eb8d02cbdf9b54c6ecd8d9d: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/be/41eca25e1ac3a8875be1856ec4bf1911c170f5`
**(No description)**
```python
<!-- ERROR reading 41eca25e1ac3a8875be1856ec4bf1911c170f5: 'utf-8' codec can't decode byte 0x89 in position 21: invalid start byte -->
```

### `.git/objects/be/662089e2ab467a161f8188d37eeb4a4fc615bf`
**(No description)**
```python
<!-- ERROR reading 662089e2ab467a161f8188d37eeb4a4fc615bf: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/be/9595c4ffc0112f2a50f264e104609ac56d5816`
**(No description)**
```python
<!-- ERROR reading 9595c4ffc0112f2a50f264e104609ac56d5816: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/be/ef4f57245b772b940e302ac480ba1039d83831`
**(No description)**
```python
<!-- ERROR reading ef4f57245b772b940e302ac480ba1039d83831: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b3/0926af8bf4f47efe98eea44d5ded4cb6f7e07d`
**(No description)**
```python
<!-- ERROR reading 0926af8bf4f47efe98eea44d5ded4cb6f7e07d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b3/16125be20aa90bc9e97a047118dd8011f5fe2f`
**(No description)**
```python
<!-- ERROR reading 16125be20aa90bc9e97a047118dd8011f5fe2f: 'utf-8' codec can't decode byte 0xf1 in position 18: invalid continuation byte -->
```

### `.git/objects/b3/16b67bd2cba2368acf9cf3f82f980dc9ce4d80`
**(No description)**
```python
<!-- ERROR reading 16b67bd2cba2368acf9cf3f82f980dc9ce4d80: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/b3/5564fbad87abd4ac1b2c20082c4716d853009d`
**(No description)**
```python
<!-- ERROR reading 5564fbad87abd4ac1b2c20082c4716d853009d: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/b3/621626cfd0264c3d82f9db02711bd17a23b994`
**(No description)**
```python
<!-- ERROR reading 621626cfd0264c3d82f9db02711bd17a23b994: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b3/626399ad0d88b0706ca87653b7cd225f2410ac`
**(No description)**
```python
<!-- ERROR reading 626399ad0d88b0706ca87653b7cd225f2410ac: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/b3/63f55a0b071de6c5f377726be82dc2110e373c`
**(No description)**
```python
<!-- ERROR reading 63f55a0b071de6c5f377726be82dc2110e373c: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/b3/67eb9ca553b1d7042169bedd31fc63267c279d`
**(No description)**
```python
<!-- ERROR reading 67eb9ca553b1d7042169bedd31fc63267c279d: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/b3/b00d2dcf3c3d795c335c0ac307689c1c1a947e`
**(No description)**
```python
<!-- ERROR reading b00d2dcf3c3d795c335c0ac307689c1c1a947e: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/b3/fee35a6cce812ad856d3b84332e73fd1973420`
**(No description)**
```python
<!-- ERROR reading fee35a6cce812ad856d3b84332e73fd1973420: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/df/673bf451f8515f9c195ff6982794847914936e`
**(No description)**
```python
<!-- ERROR reading 673bf451f8515f9c195ff6982794847914936e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/df/e07987e74dec26981b6e7d4630a5d8b65ba5e4`
**(No description)**
```python
<!-- ERROR reading e07987e74dec26981b6e7d4630a5d8b65ba5e4: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/da/052ee6983183374d074f88507b8b806a598e9b`
**(No description)**
```python
<!-- ERROR reading 052ee6983183374d074f88507b8b806a598e9b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/da/77a5af9d3e76bf368bbd6779695b3b0c8b4ef5`
**(No description)**
```python
<!-- ERROR reading 77a5af9d3e76bf368bbd6779695b3b0c8b4ef5: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/da/935846f6187a39df04f24a475cfefdb1447a8b`
**(No description)**
```python
<!-- ERROR reading 935846f6187a39df04f24a475cfefdb1447a8b: 'utf-8' codec can't decode byte 0xc2 in position 6: invalid continuation byte -->
```

### `.git/objects/da/9857e986d89acac3ba05a6735dc08c249bde1a`
**(No description)**
```python
<!-- ERROR reading 9857e986d89acac3ba05a6735dc08c249bde1a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/da/f1660f0d821143e388d37532a39ddfd2ca0347`
**(No description)**
```python
<!-- ERROR reading f1660f0d821143e388d37532a39ddfd2ca0347: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/da/fe55ca70c40e2528c08c4ee718c59debb80af2`
**(No description)**
```python
<!-- ERROR reading fe55ca70c40e2528c08c4ee718c59debb80af2: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/b4/2581dff8aabf4c2ef80ffda26296e1b368d693`
**(No description)**
```python
<!-- ERROR reading 2581dff8aabf4c2ef80ffda26296e1b368d693: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/b4/5423a4b7e8926b98790f20f1fb106114d9b856`
**(No description)**
```python
<!-- ERROR reading 5423a4b7e8926b98790f20f1fb106114d9b856: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/b4/70a373c8664325d0d00c367c0a93e926f468fa`
**(No description)**
```python
<!-- ERROR reading 70a373c8664325d0d00c367c0a93e926f468fa: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/b4/761af9b2cf384de5189269927d781a700dbe46`
**(No description)**
```python
<!-- ERROR reading 761af9b2cf384de5189269927d781a700dbe46: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/b4/76d76d9a7ff45de8d18ec22d33d6af2982f92e`
**(No description)**
```python
<!-- ERROR reading 76d76d9a7ff45de8d18ec22d33d6af2982f92e: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/b4/7dcbd4264e86715adfae1c5124c288b67a983e`
**(No description)**
```python
<!-- ERROR reading 7dcbd4264e86715adfae1c5124c288b67a983e: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/b4/996fcb1d276c48ad5637992c313e98a2bd9d99`
**(No description)**
```python
<!-- ERROR reading 996fcb1d276c48ad5637992c313e98a2bd9d99: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/b4/d7bb39562e64dd4432a131e7d9753dbabc1721`
**(No description)**
```python
<!-- ERROR reading d7bb39562e64dd4432a131e7d9753dbabc1721: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b4/f0f83c67945d3c78c167911b0d0d8aeb43af09`
**(No description)**
```python
<!-- ERROR reading f0f83c67945d3c78c167911b0d0d8aeb43af09: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/a2/2748f497f0a30fbfe7468c21e519a2887d295a`
**(No description)**
```python
<!-- ERROR reading 2748f497f0a30fbfe7468c21e519a2887d295a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/a2/c081dfc223ea4e43f30372d6ad08aee047de08`
**(No description)**
```python
<!-- ERROR reading c081dfc223ea4e43f30372d6ad08aee047de08: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/a2/d3007ceb16b0eeb4b1f57361c089558a25daeb`
**(No description)**
```python
<!-- ERROR reading d3007ceb16b0eeb4b1f57361c089558a25daeb: 'utf-8' codec can't decode byte 0xc2 in position 6: invalid continuation byte -->
```

### `.git/objects/a5/097fdb010dd243fc138fbc9780ad221fa1ce9f`
**(No description)**
```python
<!-- ERROR reading 097fdb010dd243fc138fbc9780ad221fa1ce9f: 'utf-8' codec can't decode byte 0x88 in position 19: invalid start byte -->
```

### `.git/objects/a5/20a0097c009328b6e23cdc1706080dd6167b64`
**(No description)**
```python
<!-- ERROR reading 20a0097c009328b6e23cdc1706080dd6167b64: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a5/d30f25f796cd9930d8c1aa02cca70ed25b82eb`
**(No description)**
```python
<!-- ERROR reading d30f25f796cd9930d8c1aa02cca70ed25b82eb: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/bd/1670291d6622a28ecb5b8e9ad68f4bac9305d7`
**(No description)**
```python
<!-- ERROR reading 1670291d6622a28ecb5b8e9ad68f4bac9305d7: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/bd/4692ace9b4594799974d6ecf8d44357d1d02c5`
**(No description)**
```python
<!-- ERROR reading 4692ace9b4594799974d6ecf8d44357d1d02c5: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/bd/63d98c1a3cf62c23662fcaf9953a0bc7ba890e`
**(No description)**
```python
<!-- ERROR reading 63d98c1a3cf62c23662fcaf9953a0bc7ba890e: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/bd/cdaa0bf6a28b6000517c05e53ab12f4a09c76a`
**(No description)**
```python
<!-- ERROR reading cdaa0bf6a28b6000517c05e53ab12f4a09c76a: 'utf-8' codec can't decode byte 0x8b in position 5: invalid start byte -->
```

### `.git/objects/bd/eef4e15b0dc5a68220b14c9dcec1a019401106`
**(No description)**
```python
<!-- ERROR reading eef4e15b0dc5a68220b14c9dcec1a019401106: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/d1/0282a589f3c9eb60bc520cbe5fc1bc2ddeaad6`
**(No description)**
```python
<!-- ERROR reading 0282a589f3c9eb60bc520cbe5fc1bc2ddeaad6: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d1/2a849186982399c537c5b9a8fd77bf2edd5eab`
**(No description)**
```python
<!-- ERROR reading 2a849186982399c537c5b9a8fd77bf2edd5eab: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/d1/5814fb54097403e093322512bee3ecdc7709f6`
**(No description)**
```python
<!-- ERROR reading 5814fb54097403e093322512bee3ecdc7709f6: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/d1/6552c0a9535e1c0bd7f701987301681832eba5`
**(No description)**
```python
<!-- ERROR reading 6552c0a9535e1c0bd7f701987301681832eba5: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/d1/6a60ec5b9963ef86b35a52ac92227014618e6c`
**(No description)**
```python
<!-- ERROR reading 6a60ec5b9963ef86b35a52ac92227014618e6c: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/d1/6aea1eb887caafec2165ef21c9814cb5bbb551`
**(No description)**
```python
<!-- ERROR reading 6aea1eb887caafec2165ef21c9814cb5bbb551: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d1/6e326024c05a59548619e13258acad781e0a6d`
**(No description)**
```python
<!-- ERROR reading 6e326024c05a59548619e13258acad781e0a6d: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/d1/752707598154d190d69b2c26f3098b74656652`
**(No description)**
```python
<!-- ERROR reading 752707598154d190d69b2c26f3098b74656652: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/d1/d54c0e4bd4df4a6abef26bb632a55e0d16fab7`
**(No description)**
```python
<!-- ERROR reading d54c0e4bd4df4a6abef26bb632a55e0d16fab7: 'utf-8' codec can't decode byte 0xdb in position 13: invalid continuation byte -->
```

### `.git/objects/d1/d82f157f884dc65160a41b436258d1aaf12e4c`
**(No description)**
```python
<!-- ERROR reading d82f157f884dc65160a41b436258d1aaf12e4c: 'utf-8' codec can't decode byte 0x9c in position 6: invalid start byte -->
```

### `.git/objects/d6/03d4a45a73ee4f373fbd1ef934738bda0a1991`
**(No description)**
```python
<!-- ERROR reading 03d4a45a73ee4f373fbd1ef934738bda0a1991: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d6/051297d5533a28ad80ded45a96e94462006144`
**(No description)**
```python
<!-- ERROR reading 051297d5533a28ad80ded45a96e94462006144: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/d6/45695673349e3947e8e5ae42332d0ac3164cd7`
**(No description)**
```python
<!-- ERROR reading 45695673349e3947e8e5ae42332d0ac3164cd7: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/d6/6d8566374be661085213468bce338c6a747702`
**(No description)**
```python
<!-- ERROR reading 6d8566374be661085213468bce338c6a747702: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/d6/705e22b79dd53f3896bee29eb1e2f12bf106eb`
**(No description)**
```python
<!-- ERROR reading 705e22b79dd53f3896bee29eb1e2f12bf106eb: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/d6/8eb3321270c24f479f910736957bfb785567cd`
**(No description)**
```python
<!-- ERROR reading 8eb3321270c24f479f910736957bfb785567cd: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d6/b05fefd1cfa5a4a45840664f90a3e876977727`
**(No description)**
```python
<!-- ERROR reading b05fefd1cfa5a4a45840664f90a3e876977727: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/d6/bc55d0e7e1bd9fd313d0b602b2d417891b9059`
**(No description)**
```python
<!-- ERROR reading bc55d0e7e1bd9fd313d0b602b2d417891b9059: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/d6/d2615cfdd0b914d064cdf7eecd45761e4bcaf6`
**(No description)**
```python
<!-- ERROR reading d2615cfdd0b914d064cdf7eecd45761e4bcaf6: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/d6/d3d0977dec9c5497065f85f0f77564da9eb5c7`
**(No description)**
```python
<!-- ERROR reading d3d0977dec9c5497065f85f0f77564da9eb5c7: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/bc/28d44f55bdc4b872951a74780469a3999d9ab4`
**(No description)**
```python
<!-- ERROR reading 28d44f55bdc4b872951a74780469a3999d9ab4: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/bc/50055ebd7625ded8776bba07c3a14c724c187d`
**(No description)**
```python
<!-- ERROR reading 50055ebd7625ded8776bba07c3a14c724c187d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/bc/6c3137063888e05ec4af77bed6c6fd1a3d1594`
**(No description)**
```python
<!-- ERROR reading 6c3137063888e05ec4af77bed6c6fd1a3d1594: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/bc/7f263146ee4f1701391a2436ab38e5e16f0e1a`
**(No description)**
```python
<!-- ERROR reading 7f263146ee4f1701391a2436ab38e5e16f0e1a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/bc/974e636e9f3e9b66022d2095cd670a9acbdcd9`
**(No description)**
```python
<!-- ERROR reading 974e636e9f3e9b66022d2095cd670a9acbdcd9: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/bc/aff9f57958b8c0938255fd8f937293c5850cbd`
**(No description)**
```python
<!-- ERROR reading aff9f57958b8c0938255fd8f937293c5850cbd: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/bc/be05d7efb02b3178c2a3c1cc53df401e42e063`
**(No description)**
```python
<!-- ERROR reading be05d7efb02b3178c2a3c1cc53df401e42e063: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/bc/f8906e7098a3cf82bdd87855c410e86f4f4279`
**(No description)**
```python
<!-- ERROR reading f8906e7098a3cf82bdd87855c410e86f4f4279: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/ae/4bcc8e795eba3ef15d40124b47301480f10dc8`
**(No description)**
```python
<!-- ERROR reading 4bcc8e795eba3ef15d40124b47301480f10dc8: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ae/67001af8b661373edeee2eb327b9f63e630d62`
**(No description)**
```python
<!-- ERROR reading 67001af8b661373edeee2eb327b9f63e630d62: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ae/da408e731979bf5884e4830fed142a70bfb25e`
**(No description)**
```python
<!-- ERROR reading da408e731979bf5884e4830fed142a70bfb25e: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/ae/fb5c842c2f55075546065cfba3c66d137e8184`
**(No description)**
```python
<!-- ERROR reading fb5c842c2f55075546065cfba3c66d137e8184: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d8/0a7cd4dd486d2927a3c0f2f3e684bcf5f8e49d`
**(No description)**
```python
<!-- ERROR reading 0a7cd4dd486d2927a3c0f2f3e684bcf5f8e49d: 'utf-8' codec can't decode byte 0xc9 in position 4: invalid continuation byte -->
```

### `.git/objects/d8/483ebbcd871861d1fbe4744d8ec8aa6112f42a`
**(No description)**
```python
<!-- ERROR reading 483ebbcd871861d1fbe4744d8ec8aa6112f42a: 'utf-8' codec can't decode byte 0xd0 in position 17: invalid continuation byte -->
```

### `.git/objects/d8/655b8f97e7a4e7956eefa0e129cd773a8ac372`
**(No description)**
```python
<!-- ERROR reading 655b8f97e7a4e7956eefa0e129cd773a8ac372: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/d8/846614a18d35c585ae90d397013fa9486be264`
**(No description)**
```python
<!-- ERROR reading 846614a18d35c585ae90d397013fa9486be264: 'utf-8' codec can't decode byte 0xb0 in position 10: invalid start byte -->
```

### `.git/objects/d8/b018605845977cfb10daf4e3fcaac850da6443`
**(No description)**
```python
<!-- ERROR reading b018605845977cfb10daf4e3fcaac850da6443: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/d8/b5300465bd475d9d2d1fd87e52ff867de3a445`
**(No description)**
```python
<!-- ERROR reading b5300465bd475d9d2d1fd87e52ff867de3a445: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/d8/b9936dad9ab2513fa6979f411560d3b6b57e37`
**(No description)**
```python
<!-- ERROR reading b9936dad9ab2513fa6979f411560d3b6b57e37: 'utf-8' codec can't decode byte 0xc8 in position 3: invalid continuation byte -->
```

### `.git/objects/d8/ce984c074e6f5599319d0b63cf07883422a6aa`
**(No description)**
```python
<!-- ERROR reading ce984c074e6f5599319d0b63cf07883422a6aa: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/d8/da6181b24dc8745dd39db0e0a1e252ee8d5d26`
**(No description)**
```python
<!-- ERROR reading da6181b24dc8745dd39db0e0a1e252ee8d5d26: 'utf-8' codec can't decode byte 0xb5 in position 8: invalid start byte -->
```

### `.git/objects/d8/e36b2e65d11e7f3b2c540c1b292a39a6cc219d`
**(No description)**
```python
<!-- ERROR reading e36b2e65d11e7f3b2c540c1b292a39a6cc219d: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/d8/e6fc6a9e3bbe8b9b3c032298deb08e764d32f8`
**(No description)**
```python
<!-- ERROR reading e6fc6a9e3bbe8b9b3c032298deb08e764d32f8: 'utf-8' codec can't decode byte 0x83 in position 6: invalid start byte -->
```

### `.git/objects/d8/ecefd7041a036671880673ff363651e29963f1`
**(No description)**
```python
<!-- ERROR reading ecefd7041a036671880673ff363651e29963f1: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/ab/3a4ed318eac0cab7af09312a5774dc622b0546`
**(No description)**
```python
<!-- ERROR reading 3a4ed318eac0cab7af09312a5774dc622b0546: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ab/79d16a3f4c6c894c028d1f7431811e8711b42b`
**(No description)**
```python
<!-- ERROR reading 79d16a3f4c6c894c028d1f7431811e8711b42b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/ab/82832fe4dfb246ee8d06afcbd5b70652f88e27`
**(No description)**
```python
<!-- ERROR reading 82832fe4dfb246ee8d06afcbd5b70652f88e27: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/ab/c0b2bc21a7f77c9aba1297e272c04195d4395b`
**(No description)**
```python
<!-- ERROR reading c0b2bc21a7f77c9aba1297e272c04195d4395b: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/e5/4bd4ede8761df5882a3354bc22bdee7a5e8a8b`
**(No description)**
```python
<!-- ERROR reading 4bd4ede8761df5882a3354bc22bdee7a5e8a8b: 'utf-8' codec can't decode byte 0x85 in position 12: invalid start byte -->
```

### `.git/objects/e5/534e98d69ad4151bf1eedaadf67289d8c6278d`
**(No description)**
```python
<!-- ERROR reading 534e98d69ad4151bf1eedaadf67289d8c6278d: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/e5/635887c86c4532b6af3edc57a011909b887b5a`
**(No description)**
```python
<!-- ERROR reading 635887c86c4532b6af3edc57a011909b887b5a: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/e5/6fceb14d59d2912532ad044ab4b04c96c03c2b`
**(No description)**
```python
<!-- ERROR reading 6fceb14d59d2912532ad044ab4b04c96c03c2b: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/e5/89bb917e23823e25f9fff7e0849c4d6d4a62bc`
**(No description)**
```python
<!-- ERROR reading 89bb917e23823e25f9fff7e0849c4d6d4a62bc: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/e5/a0fa400d4b36860440f8581bb34fcddbff02f6`
**(No description)**
```python
<!-- ERROR reading a0fa400d4b36860440f8581bb34fcddbff02f6: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/e5/c4e08a56f5081e87103f38b4add6ce1b730204`
**(No description)**
```python
<!-- ERROR reading c4e08a56f5081e87103f38b4add6ce1b730204: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/e2/25c4904418b1966f74f4d19cfbba801daedf87`
**(No description)**
```python
<!-- ERROR reading 25c4904418b1966f74f4d19cfbba801daedf87: 'utf-8' codec can't decode byte 0xd5 in position 3: invalid continuation byte -->
```

### `.git/objects/e2/366653791fee27408f53cc632c2decd99cfd28`
**(No description)**
```python
<!-- ERROR reading 366653791fee27408f53cc632c2decd99cfd28: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/e2/83918a6a8e8dae5bbbdb5e37550b57f2e3a30b`
**(No description)**
```python
<!-- ERROR reading 83918a6a8e8dae5bbbdb5e37550b57f2e3a30b: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/e2/8f74abef4ca5048cf1503f9a130554cf5970cf`
**(No description)**
```python
<!-- ERROR reading 8f74abef4ca5048cf1503f9a130554cf5970cf: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/e2/fd3007b1d4b3890b145f07dfa461fdd0f8e7d6`
**(No description)**
```python
<!-- ERROR reading fd3007b1d4b3890b145f07dfa461fdd0f8e7d6: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/f4/14d994d48cc385840b56f13967bd732bb54a75`
**(No description)**
```python
<!-- ERROR reading 14d994d48cc385840b56f13967bd732bb54a75: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/f4/33b1a53f5b830a205fd2df78e2b34974656c7b`
**(No description)**
```python
<!-- ERROR reading 33b1a53f5b830a205fd2df78e2b34974656c7b: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/f4/56002449f0282f42b00e255566bad83d9aa257`
**(No description)**
```python
<!-- ERROR reading 56002449f0282f42b00e255566bad83d9aa257: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/f4/6538a07f4914f373bb5f9b1ec36a0f2cc2ec50`
**(No description)**
```python
<!-- ERROR reading 6538a07f4914f373bb5f9b1ec36a0f2cc2ec50: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/f4/92464267ac54b57ee9953a4aad128f06a2110a`
**(No description)**
```python
<!-- ERROR reading 92464267ac54b57ee9953a4aad128f06a2110a: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/f4/ccea5a25653dd9e4c1bcf1047f407184562a1b`
**(No description)**
```python
<!-- ERROR reading ccea5a25653dd9e4c1bcf1047f407184562a1b: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f4/e27ab4b707f27c2e49031847b7affb7f49fe2d`
**(No description)**
```python
<!-- ERROR reading e27ab4b707f27c2e49031847b7affb7f49fe2d: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/f3/3464987bc985f1a0deea4ed4653b99f7a8d731`
**(No description)**
```python
<!-- ERROR reading 3464987bc985f1a0deea4ed4653b99f7a8d731: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/f3/3db08b6b008c91064ff0ffdc234cfc9debeb49`
**(No description)**
```python
<!-- ERROR reading 3db08b6b008c91064ff0ffdc234cfc9debeb49: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f3/451d302f514a6b2c9b4f96c6b3e17e36d7d050`
**(No description)**
```python
<!-- ERROR reading 451d302f514a6b2c9b4f96c6b3e17e36d7d050: 'utf-8' codec can't decode byte 0xb1 in position 4: invalid start byte -->
```

### `.git/objects/f3/58a448cb12739fd4eda4f4859d3a24ddd1de63`
**(No description)**
```python
<!-- ERROR reading 58a448cb12739fd4eda4f4859d3a24ddd1de63: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/f3/82ce389e802c5d6af3100ef29e882547699d65`
**(No description)**
```python
<!-- ERROR reading 82ce389e802c5d6af3100ef29e882547699d65: 'utf-8' codec can't decode byte 0xb4 in position 2: invalid start byte -->
```

### `.git/objects/f3/963fb33079fb29e374effe4b571f24dbcfcb98`
**(No description)**
```python
<!-- ERROR reading 963fb33079fb29e374effe4b571f24dbcfcb98: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/f3/9eb96e12bca844c0b00c56b40d1576934906a4`
**(No description)**
```python
<!-- ERROR reading 9eb96e12bca844c0b00c56b40d1576934906a4: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/f3/a71be04b5d87e9d776a39c69ac43a25b56596b`
**(No description)**
```python
<!-- ERROR reading a71be04b5d87e9d776a39c69ac43a25b56596b: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/f3/db2951986495e71792a69d46ed651b2e1bcb2c`
**(No description)**
```python
<!-- ERROR reading db2951986495e71792a69d46ed651b2e1bcb2c: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/f3/e06f49b4bd5a2abf1c8a78de2f78f66ff0e80a`
**(No description)**
```python
<!-- ERROR reading e06f49b4bd5a2abf1c8a78de2f78f66ff0e80a: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/eb/894327410debecb64ddf40eddc3131cf8344de`
**(No description)**
```python
<!-- ERROR reading 894327410debecb64ddf40eddc3131cf8344de: 'utf-8' codec can't decode byte 0xb4 in position 2: invalid start byte -->
```

### `.git/objects/eb/a1d127d1a2ada91fe5a77a4f12d7bea3c457c5`
**(No description)**
```python
<!-- ERROR reading a1d127d1a2ada91fe5a77a4f12d7bea3c457c5: 'utf-8' codec can't decode byte 0xb7 in position 8: invalid start byte -->
```

### `.git/objects/eb/b29b8fba1c80618cd9fa3f00c4e2229adc49cd`
**(No description)**
```python
<!-- ERROR reading b29b8fba1c80618cd9fa3f00c4e2229adc49cd: 'utf-8' codec can't decode byte 0xb2 in position 6: invalid start byte -->
```

### `.git/objects/eb/d3a97480c720d418acb1285a7b75da19b62c8c`
**(No description)**
```python
<!-- ERROR reading d3a97480c720d418acb1285a7b75da19b62c8c: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c7/0493f2b131b32378612044f30173eabbfbc3f4`
**(No description)**
```python
<!-- ERROR reading 0493f2b131b32378612044f30173eabbfbc3f4: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/c7/3eb8bbe00ceab934eff1aff2375c5df203af5f`
**(No description)**
```python
<!-- ERROR reading 3eb8bbe00ceab934eff1aff2375c5df203af5f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/c7/7c069ecc9b7f8b1f97dbcfec905725db0253a8`
**(No description)**
```python
<!-- ERROR reading 7c069ecc9b7f8b1f97dbcfec905725db0253a8: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/c7/7cde126f30c68223b1dc852928d5c2272608de`
**(No description)**
```python
<!-- ERROR reading 7cde126f30c68223b1dc852928d5c2272608de: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/c7/860808c35d544da659a48b6d04efec85b05880`
**(No description)**
```python
<!-- ERROR reading 860808c35d544da659a48b6d04efec85b05880: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/c7/ab1182f4a060117e742f4d5e721489b43c732b`
**(No description)**
```python
<!-- ERROR reading ab1182f4a060117e742f4d5e721489b43c732b: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c7/dbaed0fab5afb4f8947b24dd175d2239d35d6b`
**(No description)**
```python
<!-- ERROR reading dbaed0fab5afb4f8947b24dd175d2239d35d6b: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/c7/dc42f1d60220a4fc35aa19c76ef3c558cff9fe`
**(No description)**
```python
<!-- ERROR reading dc42f1d60220a4fc35aa19c76ef3c558cff9fe: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c7/efa801a5fce5a59e876da841c19fcdbd384bb4`
**(No description)**
```python
<!-- ERROR reading efa801a5fce5a59e876da841c19fcdbd384bb4: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/c7/f5f0577f88816469237a48df3f7ef9734e673f`
**(No description)**
```python
<!-- ERROR reading f5f0577f88816469237a48df3f7ef9734e673f: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/c7/fd5b77e6dcd00aa1dee733647fa9223c878ad1`
**(No description)**
```python
<!-- ERROR reading fd5b77e6dcd00aa1dee733647fa9223c878ad1: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/c0/0f955d941b643d4e331bf054747391189a38be`
**(No description)**
```python
<!-- ERROR reading 0f955d941b643d4e331bf054747391189a38be: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/c0/395f4a45aaa5c4ba1824a81d8ef8f69b46dc60`
**(No description)**
```python
<!-- ERROR reading 395f4a45aaa5c4ba1824a81d8ef8f69b46dc60: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/c0/56700f9fa353f25ef0d41da6e0158e3a3a4c8f`
**(No description)**
```python
<!-- ERROR reading 56700f9fa353f25ef0d41da6e0158e3a3a4c8f: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/c0/7e4a3b002c39bb29c40afdd2c3ed9f20b94595`
**(No description)**
```python
<!-- ERROR reading 7e4a3b002c39bb29c40afdd2c3ed9f20b94595: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c0/84f196525c9985084b631504586f23b18e8635`
**(No description)**
```python
<!-- ERROR reading 84f196525c9985084b631504586f23b18e8635: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/c0/940e8114a47ceacf21f4df946a6401946b9b8f`
**(No description)**
```python
<!-- ERROR reading 940e8114a47ceacf21f4df946a6401946b9b8f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c0/c57130966b6883065f8239612b73628c0562db`
**(No description)**
```python
<!-- ERROR reading c57130966b6883065f8239612b73628c0562db: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/ee/1eca3008159068c2f78226abc3b446b27c5fb9`
**(No description)**
```python
<!-- ERROR reading 1eca3008159068c2f78226abc3b446b27c5fb9: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/ee/364a904879a3cf8719e35cc6ff8b90d5fdb81b`
**(No description)**
```python
<!-- ERROR reading 364a904879a3cf8719e35cc6ff8b90d5fdb81b: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/ee/5b23494a1770bcf05c77490fd3d5f29ca37121`
**(No description)**
```python
<!-- ERROR reading 5b23494a1770bcf05c77490fd3d5f29ca37121: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/ee/a38306a9f098f400748d5786a733a5050779cc`
**(No description)**
```python
<!-- ERROR reading a38306a9f098f400748d5786a733a5050779cc: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ee/b4772649dde8aa44d6d7caecd40ef619ba814d`
**(No description)**
```python
<!-- ERROR reading b4772649dde8aa44d6d7caecd40ef619ba814d: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/ee/bdf88867dd6722eb908134cc412072b9f8b183`
**(No description)**
```python
<!-- ERROR reading bdf88867dd6722eb908134cc412072b9f8b183: 'utf-8' codec can't decode byte 0xc1 in position 3: invalid start byte -->
```

### `.git/objects/ee/c3f12f7e394a9eba2ebc43cf754a0040cdebf3`
**(No description)**
```python
<!-- ERROR reading c3f12f7e394a9eba2ebc43cf754a0040cdebf3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ee/c4d58bef558102d8b8dcc661113ae9c16bee13`
**(No description)**
```python
<!-- ERROR reading c4d58bef558102d8b8dcc661113ae9c16bee13: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/ee/face39ae62c3975ff535e6b1f79f2c28fbf888`
**(No description)**
```python
<!-- ERROR reading face39ae62c3975ff535e6b1f79f2c28fbf888: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/c9/25ae80f736ab23e07013892e1763d0d8d2b7a6`
**(No description)**
```python
<!-- ERROR reading 25ae80f736ab23e07013892e1763d0d8d2b7a6: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/c9/27cc11dc89cb57f69e62f7047140800d7ac5d2`
**(No description)**
```python
<!-- ERROR reading 27cc11dc89cb57f69e62f7047140800d7ac5d2: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c9/32313b32868c71ce3d86896fffe6d00722b35d`
**(No description)**
```python
<!-- ERROR reading 32313b32868c71ce3d86896fffe6d00722b35d: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/c9/973807e29efbcc98dcbfbecc1adbd423db6038`
**(No description)**
```python
<!-- ERROR reading 973807e29efbcc98dcbfbecc1adbd423db6038: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c9/98160e99ee1ff84827e74f6be4fe1c9d07e1d1`
**(No description)**
```python
<!-- ERROR reading 98160e99ee1ff84827e74f6be4fe1c9d07e1d1: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/c9/9c5a67945b8a3a3544d481e979c791ab45fe23`
**(No description)**
```python
<!-- ERROR reading 9c5a67945b8a3a3544d481e979c791ab45fe23: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/c9/bbda20e463b8d9389ecd65f74af33810a02bdd`
**(No description)**
```python
<!-- ERROR reading bbda20e463b8d9389ecd65f74af33810a02bdd: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/fc/29989be0b7e0f324138ca40fa31af737afe5ab`
**(No description)**
```python
<!-- ERROR reading 29989be0b7e0f324138ca40fa31af737afe5ab: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/fc/36465f5f40701bf333de8811d76d3484f211e6`
**(No description)**
```python
<!-- ERROR reading 36465f5f40701bf333de8811d76d3484f211e6: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/fc/3f2abc2440281acaae127b8352af30d68dc377`
**(No description)**
```python
<!-- ERROR reading 3f2abc2440281acaae127b8352af30d68dc377: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/fc/b99669022b04ea81a63c3dd6ac41dab208cf10`
**(No description)**
```python
<!-- ERROR reading b99669022b04ea81a63c3dd6ac41dab208cf10: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/fc/c07eec5b2e5ea926fa8b2af199e14c9cac50dd`
**(No description)**
```python
<!-- ERROR reading c07eec5b2e5ea926fa8b2af199e14c9cac50dd: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/fc/e4caa65d2eeba92acc20ab31097cb606d6c412`
**(No description)**
```python
<!-- ERROR reading e4caa65d2eeba92acc20ab31097cb606d6c412: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/fd/06ebffa3da85a874df10cf5ce3b80e9a18c4ad`
**(No description)**
```python
<!-- ERROR reading 06ebffa3da85a874df10cf5ce3b80e9a18c4ad: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/fd/1559c10e3ff25da818f893eb5e0a28c6b6d10d`
**(No description)**
```python
<!-- ERROR reading 1559c10e3ff25da818f893eb5e0a28c6b6d10d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/fd/20b2c5afdd1201256b5afe0e42d56f0de952a8`
**(No description)**
```python
<!-- ERROR reading 20b2c5afdd1201256b5afe0e42d56f0de952a8: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/fd/5d68b37f73060060db2f59bd7e9ed66f09d576`
**(No description)**
```python
<!-- ERROR reading 5d68b37f73060060db2f59bd7e9ed66f09d576: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/fd/c68c4f4a35e8d8200b3aafcda63d43839da375`
**(No description)**
```python
<!-- ERROR reading c68c4f4a35e8d8200b3aafcda63d43839da375: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/f2/5545feec199d329b5789fc5cf90f40ba18516f`
**(No description)**
```python
<!-- ERROR reading 5545feec199d329b5789fc5cf90f40ba18516f: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/f2/6bcf4d2de6eb136e31006ca3ab447d5e488adf`
**(No description)**
```python
<!-- ERROR reading 6bcf4d2de6eb136e31006ca3ab447d5e488adf: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/f2/f1d029b4c74d0dd18f4b9481078e4e87a1220a`
**(No description)**
```python
<!-- ERROR reading f1d029b4c74d0dd18f4b9481078e4e87a1220a: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/f5/1977a5ae4962f6d4a605ac40ee36eb2fc2cae6`
**(No description)**
```python
<!-- ERROR reading 1977a5ae4962f6d4a605ac40ee36eb2fc2cae6: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f5/642f79f21d872f010979dcf6f0c4a415acc19d`
**(No description)**
```python
<!-- ERROR reading 642f79f21d872f010979dcf6f0c4a415acc19d: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/f5/6ca497ee4bcd340e3905a4556e59d5434ebf26`
**(No description)**
```python
<!-- ERROR reading 6ca497ee4bcd340e3905a4556e59d5434ebf26: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/f5/903402abb5a0aed37bb23914f678ef7e34a554`
**(No description)**
```python
<!-- ERROR reading 903402abb5a0aed37bb23914f678ef7e34a554: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/f5/d5e836dd43d616c553d9bf08260054ff96b961`
**(No description)**
```python
<!-- ERROR reading d5e836dd43d616c553d9bf08260054ff96b961: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f5/d74d25f22b2360518229158af6a92c27248010`
**(No description)**
```python
<!-- ERROR reading d74d25f22b2360518229158af6a92c27248010: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/e3/312cf0caa2a8f4e6afd99435442fa01dd8cf65`
**(No description)**
```python
<!-- ERROR reading 312cf0caa2a8f4e6afd99435442fa01dd8cf65: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/e3/416d75271708b6c59c1d093f7423f592b95709`
**(No description)**
```python
<!-- ERROR reading 416d75271708b6c59c1d093f7423f592b95709: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/e3/429d2551ec705db030f9804984d65e1916a8bb`
**(No description)**
```python
<!-- ERROR reading 429d2551ec705db030f9804984d65e1916a8bb: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/e3/955954f412c11716b711a638dbf62e47e67c40`
**(No description)**
```python
<!-- ERROR reading 955954f412c11716b711a638dbf62e47e67c40: 'utf-8' codec can't decode byte 0xac in position 2: invalid start byte -->
```

### `.git/objects/e3/b0f28f0df9a9db2654a81145eae348a0fc55e7`
**(No description)**
```python
<!-- ERROR reading b0f28f0df9a9db2654a81145eae348a0fc55e7: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/e3/c6feefa22927866e3fd5575379ea972b432aaf`
**(No description)**
```python
<!-- ERROR reading c6feefa22927866e3fd5575379ea972b432aaf: 'utf-8' codec can't decode byte 0xc1 in position 3: invalid start byte -->
```

### `.git/objects/e3/e44c25b8c9deae33144ef101f2b49f2d301f5f`
**(No description)**
```python
<!-- ERROR reading e44c25b8c9deae33144ef101f2b49f2d301f5f: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/cf/12a82f193d8a69b9bc7aaa134cdbb8aa5bd938`
**(No description)**
```python
<!-- ERROR reading 12a82f193d8a69b9bc7aaa134cdbb8aa5bd938: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/cf/5156403803f9d19d484ffc14d0dc7dfd7f7bda`
**(No description)**
```python
<!-- ERROR reading 5156403803f9d19d484ffc14d0dc7dfd7f7bda: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/cf/55c8b10eb543872550be863206fe2f760d0d8d`
**(No description)**
```python
<!-- ERROR reading 55c8b10eb543872550be863206fe2f760d0d8d: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/cf/6b89448af041ed8ac2c2a76c354470ef052fbe`
**(No description)**
```python
<!-- ERROR reading 6b89448af041ed8ac2c2a76c354470ef052fbe: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/cf/8406b0fcc23477ab8b12c26977d971bac0ccf1`
**(No description)**
```python
<!-- ERROR reading 8406b0fcc23477ab8b12c26977d971bac0ccf1: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/cf/8cf7c5f078536490a3d802cf421daae962971b`
**(No description)**
```python
<!-- ERROR reading 8cf7c5f078536490a3d802cf421daae962971b: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/cf/b318d34f761cde906d8b02dde3f9329688b8c6`
**(No description)**
```python
<!-- ERROR reading b318d34f761cde906d8b02dde3f9329688b8c6: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/cf/ceb6b94ce36dad006b1f81b816d45ce70ab3d6`
**(No description)**
```python
<!-- ERROR reading ceb6b94ce36dad006b1f81b816d45ce70ab3d6: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/cf/dc030a751b089fc7e38fc88093b791605d501d`
**(No description)**
```python
<!-- ERROR reading dc030a751b089fc7e38fc88093b791605d501d: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/cf/fa4bb7db0f930f4db56653a061c4d7400ba4e6`
**(No description)**
```python
<!-- ERROR reading fa4bb7db0f930f4db56653a061c4d7400ba4e6: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/cf/fb82c536baac461a18b134a3bb7eb44b73d1ca`
**(No description)**
```python
<!-- ERROR reading fb82c536baac461a18b134a3bb7eb44b73d1ca: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/ca/0fe442d9ca499466df9438df16eca405c5f102`
**(No description)**
```python
<!-- ERROR reading 0fe442d9ca499466df9438df16eca405c5f102: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ca/15c564670271e66790000a308a7d7e981e0bac`
**(No description)**
```python
<!-- ERROR reading 15c564670271e66790000a308a7d7e981e0bac: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/ca/8a1d2d4f9e8dd4c09847b94f1d6dfe17865f76`
**(No description)**
```python
<!-- ERROR reading 8a1d2d4f9e8dd4c09847b94f1d6dfe17865f76: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/ca/b8db55d3595053898dd1edd40a1f31cc24761c`
**(No description)**
```python
<!-- ERROR reading b8db55d3595053898dd1edd40a1f31cc24761c: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ca/c7781769d567e3a8882ef7a139854be4363eab`
**(No description)**
```python
<!-- ERROR reading c7781769d567e3a8882ef7a139854be4363eab: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/e4/34c257fefd4eda43f5daf5b8dcf7d4cf9da30b`
**(No description)**
```python
<!-- ERROR reading 34c257fefd4eda43f5daf5b8dcf7d4cf9da30b: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/e4/66019b98495e2da3a1237f03cd50bfa3cd7d68`
**(No description)**
```python
<!-- ERROR reading 66019b98495e2da3a1237f03cd50bfa3cd7d68: 'utf-8' codec can't decode byte 0xdc in position 6: invalid continuation byte -->
```

### `.git/objects/e4/67c20990fef1a27c346b13acb60d1c3e7406d1`
**(No description)**
```python
<!-- ERROR reading 67c20990fef1a27c346b13acb60d1c3e7406d1: 'utf-8' codec can't decode byte 0x88 in position 21: invalid start byte -->
```

### `.git/objects/e4/aa5b827f66a5002df612738623be69206bc54c`
**(No description)**
```python
<!-- ERROR reading aa5b827f66a5002df612738623be69206bc54c: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/e4/b79b5357df88276d991231d209afb28a30b808`
**(No description)**
```python
<!-- ERROR reading b79b5357df88276d991231d209afb28a30b808: 'utf-8' codec can't decode byte 0x95 in position 3: invalid start byte -->
```

### `.git/objects/e4/b7fa3f04965a3926594d7856a71e5b76d04456`
**(No description)**
```python
<!-- ERROR reading b7fa3f04965a3926594d7856a71e5b76d04456: 'utf-8' codec can't decode byte 0x89 in position 20: invalid start byte -->
```

### `.git/objects/e4/fb27034c3df6a164bc556bf6c06055386cadd9`
**(No description)**
```python
<!-- ERROR reading fb27034c3df6a164bc556bf6c06055386cadd9: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/fe/09bb1dbb22f7670d33fe4b86ac45e207cc7eb1`
**(No description)**
```python
<!-- ERROR reading 09bb1dbb22f7670d33fe4b86ac45e207cc7eb1: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/fe/2967bd68162c74b3d73361f379bf6db5c256f0`
**(No description)**
```python
<!-- ERROR reading 2967bd68162c74b3d73361f379bf6db5c256f0: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/fe/34a7b7772cef55f5b5cb3455a2850489620ca7`
**(No description)**
```python
<!-- ERROR reading 34a7b7772cef55f5b5cb3455a2850489620ca7: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/fe/3e237cd8a118da1c707412fe8251d2e19477c5`
**(No description)**
```python
<!-- ERROR reading 3e237cd8a118da1c707412fe8251d2e19477c5: 'utf-8' codec can't decode byte 0x92 in position 8: invalid start byte -->
```

### `.git/objects/fe/49015102b3c8d6c964dc1d85e1da2b42279112`
**(No description)**
```python
<!-- ERROR reading 49015102b3c8d6c964dc1d85e1da2b42279112: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/fe/4d9c9b6c5ef3a98e4f2770d853d92d8a0124b0`
**(No description)**
```python
<!-- ERROR reading 4d9c9b6c5ef3a98e4f2770d853d92d8a0124b0: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/fe/7126463379f6ceec7b860496e16fbfddbab6c9`
**(No description)**
```python
<!-- ERROR reading 7126463379f6ceec7b860496e16fbfddbab6c9: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/fe/80d28f4658fdabdc1ec17b830fef00d20d41b3`
**(No description)**
```python
<!-- ERROR reading 80d28f4658fdabdc1ec17b830fef00d20d41b3: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/fe/86b59d782bdb09d70aa44f80370be95a667c83`
**(No description)**
```python
<!-- ERROR reading 86b59d782bdb09d70aa44f80370be95a667c83: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/fe/c627b3a36d822cd1c75336730c1ec3bb0433ed`
**(No description)**
```python
<!-- ERROR reading c627b3a36d822cd1c75336730c1ec3bb0433ed: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/fe/d59295403b80b1711d0d189ff97dde22808690`
**(No description)**
```python
<!-- ERROR reading d59295403b80b1711d0d189ff97dde22808690: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/fe/f52aa103ea369c96567b9af2a5a0ba14db5cb9`
**(No description)**
```python
<!-- ERROR reading f52aa103ea369c96567b9af2a5a0ba14db5cb9: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/c8/354ff4801101747ced1629e80c7de4a91ca07b`
**(No description)**
```python
<!-- ERROR reading 354ff4801101747ced1629e80c7de4a91ca07b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c8/4f1dd9e89407c3ba7dee18d045bc008fa8b905`
**(No description)**
```python
<!-- ERROR reading 4f1dd9e89407c3ba7dee18d045bc008fa8b905: 'utf-8' codec can't decode byte 0xfd in position 4: invalid start byte -->
```

### `.git/objects/c8/bf4e25d949184bb921df85a6657eca68041d8b`
**(No description)**
```python
<!-- ERROR reading bf4e25d949184bb921df85a6657eca68041d8b: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/c8/cceb911cf6690c2f5b1630718ef39c8f602ea0`
**(No description)**
```python
<!-- ERROR reading cceb911cf6690c2f5b1630718ef39c8f602ea0: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/c8/de5ac3542d7c402cf19bb58eff1297beecfe9a`
**(No description)**
```python
<!-- ERROR reading de5ac3542d7c402cf19bb58eff1297beecfe9a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c8/fa5f53b1743c49a935b421cd068599c4c69444`
**(No description)**
```python
<!-- ERROR reading fa5f53b1743c49a935b421cd068599c4c69444: 'utf-8' codec can't decode byte 0xb5 in position 8: invalid start byte -->
```

### `.git/objects/fb/36dc1a97a9f1f2a52c25fb6b872a7afa640be7`
**(No description)**
```python
<!-- ERROR reading 36dc1a97a9f1f2a52c25fb6b872a7afa640be7: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/fb/55ed40baf1aa3aed80750dcb3bee4d2fc69b3f`
**(No description)**
```python
<!-- ERROR reading 55ed40baf1aa3aed80750dcb3bee4d2fc69b3f: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/fb/69ac6a4d415924e4282e3d07a4cde9d4690010`
**(No description)**
```python
<!-- ERROR reading 69ac6a4d415924e4282e3d07a4cde9d4690010: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/fb/7f49cf8cd43ffae71e3e8d15174d7536f9da02`
**(No description)**
```python
<!-- ERROR reading 7f49cf8cd43ffae71e3e8d15174d7536f9da02: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/fb/d8545dc390f29604a195539b03c4022f9fa3c1`
**(No description)**
```python
<!-- ERROR reading d8545dc390f29604a195539b03c4022f9fa3c1: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/fb/dd5e41154d45a9393da5c2b8f8dec5bfcc9183`
**(No description)**
```python
<!-- ERROR reading dd5e41154d45a9393da5c2b8f8dec5bfcc9183: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/ed/0642291de4d60db0e052f4135e9e743e3b12c6`
**(No description)**
```python
<!-- ERROR reading 0642291de4d60db0e052f4135e9e743e3b12c6: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/ed/07b40f576109585f7e2b3f872edd90f718c320`
**(No description)**
```python
<!-- ERROR reading 07b40f576109585f7e2b3f872edd90f718c320: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/ed/267bf5bfd10b06d17838439b236c9eef25564d`
**(No description)**
```python
<!-- ERROR reading 267bf5bfd10b06d17838439b236c9eef25564d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ed/3e627a5769ed2be922066d72284e9026c50540`
**(No description)**
```python
<!-- ERROR reading 3e627a5769ed2be922066d72284e9026c50540: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ed/525acb33f6b286b8d46816a4559c7124e852af`
**(No description)**
```python
<!-- ERROR reading 525acb33f6b286b8d46816a4559c7124e852af: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ed/68322376db4864d2fca2d3bca0b0a300658167`
**(No description)**
```python
<!-- ERROR reading 68322376db4864d2fca2d3bca0b0a300658167: 'utf-8' codec can't decode byte 0xcb in position 4: invalid continuation byte -->
```

### `.git/objects/ed/705ce7df63140ec54a8eee1ccae2b1dcd41950`
**(No description)**
```python
<!-- ERROR reading 705ce7df63140ec54a8eee1ccae2b1dcd41950: 'utf-8' codec can't decode byte 0xb1 in position 4: invalid start byte -->
```

### `.git/objects/ed/767ba13d733a2041a57d0636d0f0ad2707ff7e`
**(No description)**
```python
<!-- ERROR reading 767ba13d733a2041a57d0636d0f0ad2707ff7e: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/ed/7a995a3aa311583efa5a47e316d4490e5f3463`
**(No description)**
```python
<!-- ERROR reading 7a995a3aa311583efa5a47e316d4490e5f3463: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/ed/8120190c06fadbc1a14b328c2ca0196046b220`
**(No description)**
```python
<!-- ERROR reading 8120190c06fadbc1a14b328c2ca0196046b220: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ed/843606feacbec3403a904a4e382fc80e727ad4`
**(No description)**
```python
<!-- ERROR reading 843606feacbec3403a904a4e382fc80e727ad4: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ed/91f404dc479d2286b1bdbd1c1423ab249cc434`
**(No description)**
```python
<!-- ERROR reading 91f404dc479d2286b1bdbd1c1423ab249cc434: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ed/c4718b686203312cea4487a30d8f7801f49b08`
**(No description)**
```python
<!-- ERROR reading c4718b686203312cea4487a30d8f7801f49b08: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/ed/e5bc14b1aaf57fcdee831d77b94d858479791b`
**(No description)**
```python
<!-- ERROR reading e5bc14b1aaf57fcdee831d77b94d858479791b: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/c1/0c6011b8358ed6de7b8e904abb44f920fe984b`
**(No description)**
```python
<!-- ERROR reading 0c6011b8358ed6de7b8e904abb44f920fe984b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c1/1a3ac39d4dd420a239c4e655140c715c5a004d`
**(No description)**
```python
<!-- ERROR reading 1a3ac39d4dd420a239c4e655140c715c5a004d: 'utf-8' codec can't decode byte 0x88 in position 17: invalid start byte -->
```

### `.git/objects/c1/238c06eab95f8c90c393383a703aa3b8c366a5`
**(No description)**
```python
<!-- ERROR reading 238c06eab95f8c90c393383a703aa3b8c366a5: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/c1/78b219def8f7fbfe6d00f7822a8e61293d003a`
**(No description)**
```python
<!-- ERROR reading 78b219def8f7fbfe6d00f7822a8e61293d003a: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c1/92a50d0b2d49a7251ef5196670477dc930506b`
**(No description)**
```python
<!-- ERROR reading 92a50d0b2d49a7251ef5196670477dc930506b: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/c1/9f83c172c46ed38cdee45031b25fa3f72a846d`
**(No description)**
```python
<!-- ERROR reading 9f83c172c46ed38cdee45031b25fa3f72a846d: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c1/a7bbf218ba985b87cd1d9b23da69222894c1dd`
**(No description)**
```python
<!-- ERROR reading a7bbf218ba985b87cd1d9b23da69222894c1dd: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/c1/aae434bc4f60042cd2702ec47525e5a1162c07`
**(No description)**
```python
<!-- ERROR reading aae434bc4f60042cd2702ec47525e5a1162c07: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/c1/b85bd71568cdb52e558c4ce103fd2cbc5a4df3`
**(No description)**
```python
<!-- ERROR reading b85bd71568cdb52e558c4ce103fd2cbc5a4df3: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/c1/d424fe084647acec00c7a0753c658f3e86ddba`
**(No description)**
```python
<!-- ERROR reading d424fe084647acec00c7a0753c658f3e86ddba: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/c1/ed80387aa4304b73c86b6635f5439151264fc3`
**(No description)**
```python
<!-- ERROR reading ed80387aa4304b73c86b6635f5439151264fc3: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/c6/1afcdb4a4d4461daf9e3506566842fcdfd078e`
**(No description)**
```python
<!-- ERROR reading 1afcdb4a4d4461daf9e3506566842fcdfd078e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c6/73d8d05bdfbbf8ba91e6d0d290cf20df581881`
**(No description)**
```python
<!-- ERROR reading 73d8d05bdfbbf8ba91e6d0d290cf20df581881: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c6/f7ed05c99d7d858e146cba778503a4aad5734d`
**(No description)**
```python
<!-- ERROR reading f7ed05c99d7d858e146cba778503a4aad5734d: 'utf-8' codec can't decode byte 0xd0 in position 22: invalid continuation byte -->
```

### `.git/objects/ec/2f44ecd4dd7988bf337cd4fd9d4c64d40c2aa2`
**(No description)**
```python
<!-- ERROR reading 2f44ecd4dd7988bf337cd4fd9d4c64d40c2aa2: 'utf-8' codec can't decode byte 0xc1 in position 3: invalid start byte -->
```

### `.git/objects/ec/7f81e22772511d668e5ab92f625db33259e803`
**(No description)**
```python
<!-- ERROR reading 7f81e22772511d668e5ab92f625db33259e803: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/ec/ca88f7dc93b78f2aa26f16cf29d17a8a83ae27`
**(No description)**
```python
<!-- ERROR reading ca88f7dc93b78f2aa26f16cf29d17a8a83ae27: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ec/f4f3be86a124478a73e7fbcb5e6e189fc53b07`
**(No description)**
```python
<!-- ERROR reading f4f3be86a124478a73e7fbcb5e6e189fc53b07: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/4e/068c9567def3564f238a76fe7ab46b569f33e5`
**(No description)**
```python
<!-- ERROR reading 068c9567def3564f238a76fe7ab46b569f33e5: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/4e/100cabb9b8d7113111d1b09a7b84da2895e2a0`
**(No description)**
```python
<!-- ERROR reading 100cabb9b8d7113111d1b09a7b84da2895e2a0: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/4e/124cce2434e02d928c8ceb8cc8eaf63e271404`
**(No description)**
```python
<!-- ERROR reading 124cce2434e02d928c8ceb8cc8eaf63e271404: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/4e/15675d8b5caa33255fe37271700f587bd26671`
**(No description)**
```python
<!-- ERROR reading 15675d8b5caa33255fe37271700f587bd26671: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/4e/15d1599bab04ac38f56cf271d2ff9b1b9984c8`
**(No description)**
```python
<!-- ERROR reading 15d1599bab04ac38f56cf271d2ff9b1b9984c8: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/4e/1926db6e7ce61e34e8003fb0c74d2321648fa9`
**(No description)**
```python
<!-- ERROR reading 1926db6e7ce61e34e8003fb0c74d2321648fa9: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/4e/b9dd65adc9aff07547f5ef7541bdf2be91124a`
**(No description)**
```python
<!-- ERROR reading b9dd65adc9aff07547f5ef7541bdf2be91124a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/20/044e4bc8f5a9775d82be0ecf387ce752732507`
**(No description)**
```python
<!-- ERROR reading 044e4bc8f5a9775d82be0ecf387ce752732507: 'utf-8' codec can't decode byte 0xf3 in position 10: invalid continuation byte -->
```

### `.git/objects/20/3578a41f3cb594252e5a1700b48999270b5b27`
**(No description)**
```python
<!-- ERROR reading 3578a41f3cb594252e5a1700b48999270b5b27: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/20/60b76ab1f314686d56014127db8445f7ef426b`
**(No description)**
```python
<!-- ERROR reading 60b76ab1f314686d56014127db8445f7ef426b: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/20/ce8f7d15bad9d48a3e0363de2286093a4a28cc`
**(No description)**
```python
<!-- ERROR reading ce8f7d15bad9d48a3e0363de2286093a4a28cc: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/20/d2770b6fecabeec22c38c28a289a18498ca7cd`
**(No description)**
```python
<!-- ERROR reading d2770b6fecabeec22c38c28a289a18498ca7cd: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/18/20722a494b1744a406e364bc3dc3aefc7dd059`
**(No description)**
```python
<!-- ERROR reading 20722a494b1744a406e364bc3dc3aefc7dd059: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/18/74a5b60de49b422a80319dfc09bb67f2ab3add`
**(No description)**
```python
<!-- ERROR reading 74a5b60de49b422a80319dfc09bb67f2ab3add: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/18/79c676d484e04e52ccbf00cf7d5a6bcfb8bd43`
**(No description)**
```python
<!-- ERROR reading 79c676d484e04e52ccbf00cf7d5a6bcfb8bd43: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/18/86d5c93426fc327a4a2e6da28a4afeb2aae540`
**(No description)**
```python
<!-- ERROR reading 86d5c93426fc327a4a2e6da28a4afeb2aae540: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/18/b81340a7f74b2762db3b2db6b1ab1414df01ca`
**(No description)**
```python
<!-- ERROR reading b81340a7f74b2762db3b2db6b1ab1414df01ca: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/18/e45c6921c562f46d1e044fccf84320dcce320d`
**(No description)**
```python
<!-- ERROR reading e45c6921c562f46d1e044fccf84320dcce320d: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/18/ec666f1b59f69d6f6c9ba672ddd8f1ce94b484`
**(No description)**
```python
<!-- ERROR reading ec666f1b59f69d6f6c9ba672ddd8f1ce94b484: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/18/f7c999bee0fab95293b2434047fd20532a6446`
**(No description)**
```python
<!-- ERROR reading f7c999bee0fab95293b2434047fd20532a6446: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/27/01747f56cc77845159f2c5fee2d0ce114259af`
**(No description)**
```python
<!-- ERROR reading 01747f56cc77845159f2c5fee2d0ce114259af: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/27/15b192dab03666a69db65d983a67711e717c62`
**(No description)**
```python
<!-- ERROR reading 15b192dab03666a69db65d983a67711e717c62: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/27/49b12c0ebaf4ef92e6a77c374543b7e343f3ba`
**(No description)**
```python
<!-- ERROR reading 49b12c0ebaf4ef92e6a77c374543b7e343f3ba: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/27/c6baf433f9dff26ee18cff03658a6346162a9a`
**(No description)**
```python
<!-- ERROR reading c6baf433f9dff26ee18cff03658a6346162a9a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/4b/00fcb60173c5497fb24839da1837e8bdbfd98c`
**(No description)**
```python
<!-- ERROR reading 00fcb60173c5497fb24839da1837e8bdbfd98c: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/4b/065e49a19d6023cb11bc55870d7db956e5f6e3`
**(No description)**
```python
<!-- ERROR reading 065e49a19d6023cb11bc55870d7db956e5f6e3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/4b/0732f4c7fd450fa11e0d7436d113edc43378b7`
**(No description)**
```python
<!-- ERROR reading 0732f4c7fd450fa11e0d7436d113edc43378b7: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/4b/825dc642cb6eb9a060e54bf8d69288fbee4904`
**(No description)**
```python
x+)JMU0`  
,
```

### `.git/objects/4b/8e4b359f3149bc45e18d293a2a2772a174e235`
**(No description)**
```python
<!-- ERROR reading 8e4b359f3149bc45e18d293a2a2772a174e235: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/4b/e1a09cb3214fdacae75ddc01d05746fc8ebc23`
**(No description)**
```python
<!-- ERROR reading e1a09cb3214fdacae75ddc01d05746fc8ebc23: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/4b/e6004622efcdc36a8d15efc0ac3e138a4bae02`
**(No description)**
```python
<!-- ERROR reading e6004622efcdc36a8d15efc0ac3e138a4bae02: 'utf-8' codec can't decode byte 0x9d in position 3: invalid start byte -->
```

### `.git/objects/pack/pack-4b94e9193a231835256bb031f03fe7d1cac01bc5.idx`
**(No description)**
```python
<!-- ERROR reading pack-4b94e9193a231835256bb031f03fe7d1cac01bc5.idx: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte -->
```

### `.git/objects/pack/pack-4b94e9193a231835256bb031f03fe7d1cac01bc5.pack`
**(No description)**
```python
<!-- ERROR reading pack-4b94e9193a231835256bb031f03fe7d1cac01bc5.pack: 'utf-8' codec can't decode byte 0xc1 in position 11: invalid start byte -->
```

### `.git/objects/pack/pack-4b94e9193a231835256bb031f03fe7d1cac01bc5.rev`
**(No description)**
```python
<!-- ERROR reading pack-4b94e9193a231835256bb031f03fe7d1cac01bc5.rev: 'utf-8' codec can't decode byte 0x9b in position 19: invalid start byte -->
```

### `.git/objects/11/467eeda9b317cbf5d378beea30e31a51d35d1c`
**(No description)**
```python
<!-- ERROR reading 467eeda9b317cbf5d378beea30e31a51d35d1c: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/11/51a1954d069a3bb5035954c9ee7387c2e53298`
**(No description)**
```python
<!-- ERROR reading 51a1954d069a3bb5035954c9ee7387c2e53298: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/11/b259170c6d095aeb878927e7f34c5c941dab0f`
**(No description)**
```python
<!-- ERROR reading b259170c6d095aeb878927e7f34c5c941dab0f: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/11/bdb5c1f5fcdd91af5d587c352039cb8476af49`
**(No description)**
```python
<!-- ERROR reading bdb5c1f5fcdd91af5d587c352039cb8476af49: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/11/daea9f04e2395b4dcf497c3fd1488bcff256fe`
**(No description)**
```python
<!-- ERROR reading daea9f04e2395b4dcf497c3fd1488bcff256fe: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/11/ec695ff79627463a0282d25079527562de9e42`
**(No description)**
```python
<!-- ERROR reading ec695ff79627463a0282d25079527562de9e42: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/7d/170dd27731a5c0d3065e017a061b8c3607e982`
**(No description)**
```python
<!-- ERROR reading 170dd27731a5c0d3065e017a061b8c3607e982: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/7d/1e8c20fb09ddaa0254ae74cbd4425ffdc5dcdc`
**(No description)**
```python
<!-- ERROR reading 1e8c20fb09ddaa0254ae74cbd4425ffdc5dcdc: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/7d/1f0f29cba8e282e19eb031702251a489b72a7d`
**(No description)**
```python
<!-- ERROR reading 1f0f29cba8e282e19eb031702251a489b72a7d: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/7d/4bf87e7208b0b536d5f4879bbcf4bace79763f`
**(No description)**
```python
<!-- ERROR reading 4bf87e7208b0b536d5f4879bbcf4bace79763f: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/7d/62991ff8280315a3a9aae4678c81f3f2c9f6d4`
**(No description)**
```python
<!-- ERROR reading 62991ff8280315a3a9aae4678c81f3f2c9f6d4: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/7d/6ece8001dc61ec804313e549771bf284a99b37`
**(No description)**
```python
<!-- ERROR reading 6ece8001dc61ec804313e549771bf284a99b37: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/7d/9666844e4e712641a32408a2e2cfdb895455e5`
**(No description)**
```python
<!-- ERROR reading 9666844e4e712641a32408a2e2cfdb895455e5: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/7d/a7eb3184244235f16869ca279b518c5b1ed991`
**(No description)**
```python
<!-- ERROR reading a7eb3184244235f16869ca279b518c5b1ed991: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/7d/ac55b601eef6950ddf24be9170f1656cb15366`
**(No description)**
```python
<!-- ERROR reading ac55b601eef6950ddf24be9170f1656cb15366: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/7d/be8cef54a692c49e5fd01ddb5d01b224ee2d6d`
**(No description)**
```python
<!-- ERROR reading be8cef54a692c49e5fd01ddb5d01b224ee2d6d: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/7d/c04a746064897e5448a6625ae3cfe71ef425e3`
**(No description)**
```python
<!-- ERROR reading c04a746064897e5448a6625ae3cfe71ef425e3: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/29/2f2d7b01dd6e8e41e8fad4b12a90479d022897`
**(No description)**
```python
<!-- ERROR reading 2f2d7b01dd6e8e41e8fad4b12a90479d022897: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/29/5dc928ba71fc00caa52708ac70097abe6dc3e4`
**(No description)**
```python
<!-- ERROR reading 5dc928ba71fc00caa52708ac70097abe6dc3e4: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/29/85419abf23f5e529af43883f1d365452e4190a`
**(No description)**
```python
<!-- ERROR reading 85419abf23f5e529af43883f1d365452e4190a: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/29/9015d4fef268cde91273790251f35192e1c8a6`
**(No description)**
```python
<!-- ERROR reading 9015d4fef268cde91273790251f35192e1c8a6: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/29/9f4c7d02e7763fc563560f3452b048d89f075d`
**(No description)**
```python
<!-- ERROR reading 9f4c7d02e7763fc563560f3452b048d89f075d: 'utf-8' codec can't decode byte 0xdd in position 4: invalid continuation byte -->
```

### `.git/objects/29/cbf91ef79b89971e51db9ddfc3720d8b4db82a`
**(No description)**
```python
<!-- ERROR reading cbf91ef79b89971e51db9ddfc3720d8b4db82a: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/29/f0662f88d495cdf87c1f3e94d1e17fedcf772f`
**(No description)**
```python
<!-- ERROR reading f0662f88d495cdf87c1f3e94d1e17fedcf772f: 'utf-8' codec can't decode byte 0x8d in position 22: invalid start byte -->
```

### `.git/objects/7c/0edd1b722cd755a16b3bf1ab543c739bc16688`
**(No description)**
```python
<!-- ERROR reading 0edd1b722cd755a16b3bf1ab543c739bc16688: 'utf-8' codec can't decode byte 0x8c in position 2: invalid start byte -->
```

### `.git/objects/7c/2344bf3bfdb23bc57d0dbed711393285ad800a`
**(No description)**
```python
<!-- ERROR reading 2344bf3bfdb23bc57d0dbed711393285ad800a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/7c/3609de6707ee3707ef65902ac75879fbe05c86`
**(No description)**
```python
<!-- ERROR reading 3609de6707ee3707ef65902ac75879fbe05c86: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/7c/50ed76dc4d8df41262973a0122295523e2a935`
**(No description)**
```python
<!-- ERROR reading 50ed76dc4d8df41262973a0122295523e2a935: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/7c/d12cdf5507e16880167f42813282744581b993`
**(No description)**
```python
<!-- ERROR reading d12cdf5507e16880167f42813282744581b993: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/7c/ef957e41174e3e8b7798c78f497df5b7ccd998`
**(No description)**
```python
<!-- ERROR reading ef957e41174e3e8b7798c78f497df5b7ccd998: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/7c/f88ba113cd211b4c7e90cc152b07696274fda2`
**(No description)**
```python
<!-- ERROR reading f88ba113cd211b4c7e90cc152b07696274fda2: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/16/02bdf8eec078ad3348d458accc18e15e1cfb51`
**(No description)**
```python
<!-- ERROR reading 02bdf8eec078ad3348d458accc18e15e1cfb51: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/16/424e7050f73705bf2d08b50c466f70c514ca8d`
**(No description)**
```python
<!-- ERROR reading 424e7050f73705bf2d08b50c466f70c514ca8d: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/16/b5bfc49b9846701c2cb7328fac03f85a280727`
**(No description)**
```python
<!-- ERROR reading b5bfc49b9846701c2cb7328fac03f85a280727: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/16/b94482c061f69e3ad415f1908ad2da715d1304`
**(No description)**
```python
<!-- ERROR reading b94482c061f69e3ad415f1908ad2da715d1304: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/16/ba5290faef35e77277fddb1afd0c48573bc54d`
**(No description)**
```python
<!-- ERROR reading ba5290faef35e77277fddb1afd0c48573bc54d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/16/c275393728221d6d4ab3cd6e495c70091ec7f5`
**(No description)**
```python
<!-- ERROR reading c275393728221d6d4ab3cd6e495c70091ec7f5: 'utf-8' codec can't decode byte 0x88 in position 19: invalid start byte -->
```

### `.git/objects/42/08460843e247b315e54465cd0df3f78d5dca2e`
**(No description)**
```python
<!-- ERROR reading 08460843e247b315e54465cd0df3f78d5dca2e: 'utf-8' codec can't decode byte 0xcc in position 3: invalid continuation byte -->
```

### `.git/objects/42/39aaaf0914f8264bb8614a3762302a5f698a4a`
**(No description)**
```python
<!-- ERROR reading 39aaaf0914f8264bb8614a3762302a5f698a4a: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/42/484423c9ef7b6f02f715e06ee9de81eb91a927`
**(No description)**
```python
<!-- ERROR reading 484423c9ef7b6f02f715e06ee9de81eb91a927: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/42/526be7f55fa9640a4f7ccc245f7299f9483e6b`
**(No description)**
```python
<!-- ERROR reading 526be7f55fa9640a4f7ccc245f7299f9483e6b: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/42/b68773b146c4c94432c908addebd7a54e14294`
**(No description)**
```python
<!-- ERROR reading b68773b146c4c94432c908addebd7a54e14294: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/42/ce7b75c92fb01a3f6ed17eea363f756b7da582`
**(No description)**
```python
<!-- ERROR reading ce7b75c92fb01a3f6ed17eea363f756b7da582: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/42/f080845cfa21d0c7b31d788badb800f0b81525`
**(No description)**
```python
<!-- ERROR reading f080845cfa21d0c7b31d788badb800f0b81525: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/89/19aa538ddcd2bbffd2140570d55613e4c5f209`
**(No description)**
```python
<!-- ERROR reading 19aa538ddcd2bbffd2140570d55613e4c5f209: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/89/32a18e4596952373a38c60b81b7116d4ef9ee8`
**(No description)**
```python
<!-- ERROR reading 32a18e4596952373a38c60b81b7116d4ef9ee8: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/89/3f872964c2e6df9a81fdba3dd8fadfeaab9731`
**(No description)**
```python
<!-- ERROR reading 3f872964c2e6df9a81fdba3dd8fadfeaab9731: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/89/41572b3e6a2a2267659ed74e25099c37aae90b`
**(No description)**
```python
<!-- ERROR reading 41572b3e6a2a2267659ed74e25099c37aae90b: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/89/45b5da857f4a7dec2b84f1225f012f6098418c`
**(No description)**
```python
<!-- ERROR reading 45b5da857f4a7dec2b84f1225f012f6098418c: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/89/690eb8ea17da3dbd83c5250d635c10b12a9e7d`
**(No description)**
```python
<!-- ERROR reading 690eb8ea17da3dbd83c5250d635c10b12a9e7d: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/89/76a375735f4c48c98883397ebd559cbbd22ce6`
**(No description)**
```python
<!-- ERROR reading 76a375735f4c48c98883397ebd559cbbd22ce6: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/89/9dfada878e1181fca6d3c75a79526a076abb9e`
**(No description)**
```python
<!-- ERROR reading 9dfada878e1181fca6d3c75a79526a076abb9e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/89/b8602443ff5d97b2c4f193c0f51c82f58e3469`
**(No description)**
```python
<!-- ERROR reading b8602443ff5d97b2c4f193c0f51c82f58e3469: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/89/cc0e94d3bc781cfa59a0dc89c78e76afa1f5e4`
**(No description)**
```python
<!-- ERROR reading cc0e94d3bc781cfa59a0dc89c78e76afa1f5e4: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/89/d041605c006e326a67f399a58a1fec8eb24acf`
**(No description)**
```python
<!-- ERROR reading d041605c006e326a67f399a58a1fec8eb24acf: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/45/010b257ea7630118d90a17356164b9f70bcc19`
**(No description)**
```python
<!-- ERROR reading 010b257ea7630118d90a17356164b9f70bcc19: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/45/1ea0760f07bc2a70029b99b124883b42a92f9c`
**(No description)**
```python
<!-- ERROR reading 1ea0760f07bc2a70029b99b124883b42a92f9c: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/45/2a9244ea6766d8cf94425fb583583ef740baee`
**(No description)**
```python
<!-- ERROR reading 2a9244ea6766d8cf94425fb583583ef740baee: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/45/399766797f553288b831007d5cbc917780dc89`
**(No description)**
```python
<!-- ERROR reading 399766797f553288b831007d5cbc917780dc89: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/45/47fc522b690ba2697843edd044f2039a4123a9`
**(No description)**
```python
<!-- ERROR reading 47fc522b690ba2697843edd044f2039a4123a9: 'utf-8' codec can't decode byte 0x93 in position 3: invalid start byte -->
```

### `.git/objects/45/51d6887221990e5b6b613a9502d727b6755c34`
**(No description)**
```python
<!-- ERROR reading 51d6887221990e5b6b613a9502d727b6755c34: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/45/628cbc838028bc1120e3302429ad9556a0ff33`
**(No description)**
```python
<!-- ERROR reading 628cbc838028bc1120e3302429ad9556a0ff33: 'utf-8' codec can't decode byte 0xaa in position 6: invalid start byte -->
```

### `.git/objects/45/6599b8f81f45f9d80bdaff01508e63d4eece7f`
**(No description)**
```python
<!-- ERROR reading 6599b8f81f45f9d80bdaff01508e63d4eece7f: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/45/7481e3258bffef81125f0ccc3caa461a9c2c9b`
**(No description)**
```python
<!-- ERROR reading 7481e3258bffef81125f0ccc3caa461a9c2c9b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/45/8ca08f796d9b1d13494c675dd59c87d1ef8d99`
**(No description)**
```python
<!-- ERROR reading 8ca08f796d9b1d13494c675dd59c87d1ef8d99: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/45/9bbe095b2765a77519ed2767ca53cb336e438c`
**(No description)**
```python
<!-- ERROR reading 9bbe095b2765a77519ed2767ca53cb336e438c: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/1f/11935c70e9a7ce3f453143895e9c48e19b38ed`
**(No description)**
```python
<!-- ERROR reading 11935c70e9a7ce3f453143895e9c48e19b38ed: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/1f/516e2a41972f5496a2c8486ad67890a27820c2`
**(No description)**
```python
<!-- ERROR reading 516e2a41972f5496a2c8486ad67890a27820c2: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/1f/89992eed8b6995bb00b9763840a3ac5e5c87e0`
**(No description)**
```python
<!-- ERROR reading 89992eed8b6995bb00b9763840a3ac5e5c87e0: 'utf-8' codec can't decode byte 0x9e in position 9: invalid start byte -->
```

### `.git/objects/1f/bf55bdfbb882d6defcda103111e0363ec41ab8`
**(No description)**
```python
<!-- ERROR reading bf55bdfbb882d6defcda103111e0363ec41ab8: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/73/06c04ead7e14bef119182d92d959a9ee8538a5`
**(No description)**
```python
<!-- ERROR reading 06c04ead7e14bef119182d92d959a9ee8538a5: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/73/0a746843b98732f964e7b4111b30782b99c0c3`
**(No description)**
```python
<!-- ERROR reading 0a746843b98732f964e7b4111b30782b99c0c3: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/73/0bbf2aecc31e97a3646def2eb91c510bdec840`
**(No description)**
```python
<!-- ERROR reading 0bbf2aecc31e97a3646def2eb91c510bdec840: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/73/3ef8d6650df9b401c93a63914a204045d8d2ba`
**(No description)**
```python
<!-- ERROR reading 3ef8d6650df9b401c93a63914a204045d8d2ba: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/73/9568d74d0f6d07573eea36d79beca155afbe25`
**(No description)**
```python
<!-- ERROR reading 9568d74d0f6d07573eea36d79beca155afbe25: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/73/a27b98bebd949cb3b99e19a3a8a484455b58d7`
**(No description)**
```python
<!-- ERROR reading a27b98bebd949cb3b99e19a3a8a484455b58d7: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/73/d2aca7e698f7703e354534d9c6d367dbc7cf5b`
**(No description)**
```python
<!-- ERROR reading d2aca7e698f7703e354534d9c6d367dbc7cf5b: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/73/e493434e4114c5924fd2a0ce87229ce851d487`
**(No description)**
```python
<!-- ERROR reading e493434e4114c5924fd2a0ce87229ce851d487: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/87/062b8187fa4f74a8c4edbaa60bd9a8b2d506a4`
**(No description)**
```python
<!-- ERROR reading 062b8187fa4f74a8c4edbaa60bd9a8b2d506a4: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/87/65b907d70c4a530bc90dc88f24b3df73473b01`
**(No description)**
```python
<!-- ERROR reading 65b907d70c4a530bc90dc88f24b3df73473b01: 'utf-8' codec can't decode byte 0xdc in position 6: invalid continuation byte -->
```

### `.git/objects/87/844403b8150561722b713584b08d9162823f1e`
**(No description)**
```python
<!-- ERROR reading 844403b8150561722b713584b08d9162823f1e: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/87/9b6981ed444e709f5b412c262a4afcb4496374`
**(No description)**
```python
<!-- ERROR reading 9b6981ed444e709f5b412c262a4afcb4496374: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/87/e4e6214098778794fac588138c8fa588787425`
**(No description)**
```python
<!-- ERROR reading e4e6214098778794fac588138c8fa588787425: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/80/00967eafc52526b43e451106a15996c46969c9`
**(No description)**
```python
<!-- ERROR reading 00967eafc52526b43e451106a15996c46969c9: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/80/01c4722f881b3a4cee13c1aa82c8a150b992c8`
**(No description)**
```python
<!-- ERROR reading 01c4722f881b3a4cee13c1aa82c8a150b992c8: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/80/0d5c5588c99dc216cdea5084da440efb641945`
**(No description)**
```python
<!-- ERROR reading 0d5c5588c99dc216cdea5084da440efb641945: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/80/136766612aefce6293c550acd3044434f2b277`
**(No description)**
```python
<!-- ERROR reading 136766612aefce6293c550acd3044434f2b277: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/80/1a763e659ae28426351b4eda79bb35ac974549`
**(No description)**
```python
<!-- ERROR reading 1a763e659ae28426351b4eda79bb35ac974549: 'utf-8' codec can't decode byte 0xc8 in position 18: invalid continuation byte -->
```

### `.git/objects/80/1bfacf671017cfbebf1ac26ec385daa02ed260`
**(No description)**
```python
<!-- ERROR reading 1bfacf671017cfbebf1ac26ec385daa02ed260: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/80/1ea1412479df35341cd0fb5c5301b6d52ee614`
**(No description)**
```python
<!-- ERROR reading 1ea1412479df35341cd0fb5c5301b6d52ee614: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/80/2cea9bd5e20e66449f4cf2326121480dc53206`
**(No description)**
```python
<!-- ERROR reading 2cea9bd5e20e66449f4cf2326121480dc53206: 'utf-8' codec can't decode byte 0x85 in position 14: invalid start byte -->
```

### `.git/objects/80/3363ca2f34eb9b57702d3f7ed02258fd0c1610`
**(No description)**
```python
<!-- ERROR reading 3363ca2f34eb9b57702d3f7ed02258fd0c1610: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/80/6c98da869a203706670056c9cf3df3f1dfe460`
**(No description)**
```python
<!-- ERROR reading 6c98da869a203706670056c9cf3df3f1dfe460: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/80/8646cc27216c3423681041ee9923372a2a9d03`
**(No description)**
```python
<!-- ERROR reading 8646cc27216c3423681041ee9923372a2a9d03: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/80/ad2546d7981394b5f5d221336c9f00236b9d66`
**(No description)**
```python
<!-- ERROR reading ad2546d7981394b5f5d221336c9f00236b9d66: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/80/c474c4e939c149a22e811a5a1a5419313b7cc7`
**(No description)**
```python
<!-- ERROR reading c474c4e939c149a22e811a5a1a5419313b7cc7: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/80/d836b059202757ca019ac0ed975e24c9582c06`
**(No description)**
```python
<!-- ERROR reading d836b059202757ca019ac0ed975e24c9582c06: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/80/eb783da936dd8ce312bff8bf682d5681deca89`
**(No description)**
```python
<!-- ERROR reading eb783da936dd8ce312bff8bf682d5681deca89: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/80/f0bee2994632dc33a25da7b839522da2119393`
**(No description)**
```python
<!-- ERROR reading f0bee2994632dc33a25da7b839522da2119393: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/80/f64a2e8e5763ae327c5c213ec12e24f023b4d3`
**(No description)**
```python
<!-- ERROR reading f64a2e8e5763ae327c5c213ec12e24f023b4d3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/74/1c4adcae44a86becf67b38719ae52dcb24b57f`
**(No description)**
```python
<!-- ERROR reading 1c4adcae44a86becf67b38719ae52dcb24b57f: 'utf-8' codec can't decode byte 0x88 in position 19: invalid start byte -->
```

### `.git/objects/74/554b1e2a149c37131168fbe283f3e2476a8f75`
**(No description)**
```python
<!-- ERROR reading 554b1e2a149c37131168fbe283f3e2476a8f75: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/74/5f0d7b346a1aac57197ab99d3d7d8b207b890a`
**(No description)**
```python
<!-- ERROR reading 5f0d7b346a1aac57197ab99d3d7d8b207b890a: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/74/795ba922bb376e24858760e63dc9124ef22b9f`
**(No description)**
```python
<!-- ERROR reading 795ba922bb376e24858760e63dc9124ef22b9f: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/74/79843822351e8fd1a53fa3633756c06deb5415`
**(No description)**
```python
<!-- ERROR reading 79843822351e8fd1a53fa3633756c06deb5415: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/74/83be27d4d24f845e56b6954ee63eec730c00aa`
**(No description)**
```python
<!-- ERROR reading 83be27d4d24f845e56b6954ee63eec730c00aa: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/74/d225472f6f62727fd2e4d698f77cf3137725e8`
**(No description)**
```python
<!-- ERROR reading d225472f6f62727fd2e4d698f77cf3137725e8: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/74/e0deeab3f5904260ac2d36d64fbdec7e0ee0bf`
**(No description)**
```python
<!-- ERROR reading e0deeab3f5904260ac2d36d64fbdec7e0ee0bf: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/1a/01d62f7c08fb7922ae5b5fb53edc2b461ed534`
**(No description)**
```python
<!-- ERROR reading 01d62f7c08fb7922ae5b5fb53edc2b461ed534: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/1a/c01dde512efb9b82520b1d4cdf2026f09bde54`
**(No description)**
```python
<!-- ERROR reading c01dde512efb9b82520b1d4cdf2026f09bde54: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/1a/e51cd11ea475060a6f6c46e755c2b9f429b3da`
**(No description)**
```python
<!-- ERROR reading e51cd11ea475060a6f6c46e755c2b9f429b3da: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/28/1ea1c2af6b0eb5f02ecc6d115f2d6884be74b5`
**(No description)**
```python
<!-- ERROR reading 1ea1c2af6b0eb5f02ecc6d115f2d6884be74b5: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/28/56d85d19550422abb91ee35f11f461b5b315d7`
**(No description)**
```python
<!-- ERROR reading 56d85d19550422abb91ee35f11f461b5b315d7: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/28/7d2bcb558a5b2b819bade62e9745921e5121ef`
**(No description)**
```python
<!-- ERROR reading 7d2bcb558a5b2b819bade62e9745921e5121ef: 'utf-8' codec can't decode byte 0x88 in position 17: invalid start byte -->
```

### `.git/objects/28/8676e114f662d38c2d172de8806df190c6b318`
**(No description)**
```python
<!-- ERROR reading 8676e114f662d38c2d172de8806df190c6b318: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/17/098cca580d7a19c1705987bc06172bc3b39b8d`
**(No description)**
```python
<!-- ERROR reading 098cca580d7a19c1705987bc06172bc3b39b8d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/17/31a4b8d0df259f3768730d5506714c2460e89e`
**(No description)**
```python
<!-- ERROR reading 31a4b8d0df259f3768730d5506714c2460e89e: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/17/46bd01c1ad915b728ab58b4668c82b2bd578e1`
**(No description)**
```python
<!-- ERROR reading 46bd01c1ad915b728ab58b4668c82b2bd578e1: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/17/7082e0fb151364bf7ff5e801eadabf8734acfc`
**(No description)**
```python
<!-- ERROR reading 7082e0fb151364bf7ff5e801eadabf8734acfc: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/17/936e3e71c73c4d4855445074ef2b62c10c0901`
**(No description)**
```python
<!-- ERROR reading 936e3e71c73c4d4855445074ef2b62c10c0901: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/17/a00ba7dbb70598c3fdd7b176b260334f4de572`
**(No description)**
```python
<!-- ERROR reading a00ba7dbb70598c3fdd7b176b260334f4de572: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/17/ec30f526d581d0923b15808e2d6138ca91b38e`
**(No description)**
```python
<!-- ERROR reading ec30f526d581d0923b15808e2d6138ca91b38e: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/7b/24908a5e61dd1c90564853a1f026c874a31549`
**(No description)**
```python
<!-- ERROR reading 24908a5e61dd1c90564853a1f026c874a31549: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/7b/51052c9a2517710729cd9ad32c42d85a3b3e79`
**(No description)**
```python
<!-- ERROR reading 51052c9a2517710729cd9ad32c42d85a3b3e79: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/7b/5f310fe2211e5be1706ce11a4ee5c8ad327af8`
**(No description)**
```python
<!-- ERROR reading 5f310fe2211e5be1706ce11a4ee5c8ad327af8: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/7b/6165358c5e372630f3b54d6c684b54e0dfaf1a`
**(No description)**
```python
<!-- ERROR reading 6165358c5e372630f3b54d6c684b54e0dfaf1a: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/7b/7dd9eddd31fae557af8861da98f79baf20f8bb`
**(No description)**
```python
<!-- ERROR reading 7dd9eddd31fae557af8861da98f79baf20f8bb: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/7b/faa8d80d7dc471d572db0f949460901126e8bd`
**(No description)**
```python
<!-- ERROR reading faa8d80d7dc471d572db0f949460901126e8bd: 'utf-8' codec can't decode byte 0xe3 in position 6: invalid continuation byte -->
```

### `.git/objects/8f/03e146506dbb51c774f0d8e33a95e5f32c227d`
**(No description)**
```python
<!-- ERROR reading 03e146506dbb51c774f0d8e33a95e5f32c227d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/8f/080eae848f759c9173bfc0c79506357ebe5090`
**(No description)**
```python
<!-- ERROR reading 080eae848f759c9173bfc0c79506357ebe5090: 'utf-8' codec can't decode byte 0xdb in position 4: invalid continuation byte -->
```

### `.git/objects/8f/5601dd31e53804bb3c4de6e577d8612b79bcb1`
**(No description)**
```python
<!-- ERROR reading 5601dd31e53804bb3c4de6e577d8612b79bcb1: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/8f/6c890635838b1d91a67a5647cb0117fcda96a4`
**(No description)**
```python
<!-- ERROR reading 6c890635838b1d91a67a5647cb0117fcda96a4: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/8f/7731af0e62a985dbe4c77771a80525848e793c`
**(No description)**
```python
<!-- ERROR reading 7731af0e62a985dbe4c77771a80525848e793c: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/8f/7c3b4f51beea0866f6485998bc8398b13bdffa`
**(No description)**
```python
<!-- ERROR reading 7c3b4f51beea0866f6485998bc8398b13bdffa: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/8f/8b09bd23935eae4c03cfe7116b12d8eacdee2f`
**(No description)**
```python
<!-- ERROR reading 8b09bd23935eae4c03cfe7116b12d8eacdee2f: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/8f/b65c8e68268cfcc0521dc9719ff02947fe2c21`
**(No description)**
```python
<!-- ERROR reading b65c8e68268cfcc0521dc9719ff02947fe2c21: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/8a/1dc979a39e36ce81e987843391479f125d73f3`
**(No description)**
```python
<!-- ERROR reading 1dc979a39e36ce81e987843391479f125d73f3: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/8a/2e993a582eb7afc11d9e051d4392c94c6d3ba5`
**(No description)**
```python
<!-- ERROR reading 2e993a582eb7afc11d9e051d4392c94c6d3ba5: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/8a/65f13347d6621289a166d08123cbc8e1ad0157`
**(No description)**
```python
<!-- ERROR reading 65f13347d6621289a166d08123cbc8e1ad0157: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/8a/7ecb83311156dc276649f8e6701cbdf4d15fdf`
**(No description)**
```python
<!-- ERROR reading 7ecb83311156dc276649f8e6701cbdf4d15fdf: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/8a/7f3266c4db7eed088ad84ed8a91684362a41e6`
**(No description)**
```python
<!-- ERROR reading 7f3266c4db7eed088ad84ed8a91684362a41e6: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/8a/acf8120147c457dccd4b955fd898c3f5a90ba9`
**(No description)**
```python
<!-- ERROR reading acf8120147c457dccd4b955fd898c3f5a90ba9: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/8a/e96007f7d725813fd02dc1d06d3834ee1939e4`
**(No description)**
```python
<!-- ERROR reading e96007f7d725813fd02dc1d06d3834ee1939e4: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/8a/e9c408482aefeffad0b6620ca69166f4b13e76`
**(No description)**
```python
<!-- ERROR reading e9c408482aefeffad0b6620ca69166f4b13e76: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/7e/535454bbeae5491438ef504b5517a08997f6a2`
**(No description)**
```python
<!-- ERROR reading 535454bbeae5491438ef504b5517a08997f6a2: 'utf-8' codec can't decode byte 0xbd in position 16: invalid start byte -->
```

### `.git/objects/7e/bc7eb994bba9ed32f30d557af93627cae4d543`
**(No description)**
```python
<!-- ERROR reading bc7eb994bba9ed32f30d557af93627cae4d543: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/7e/f51b92e1d9cbbcf0aa3dc46b892c08fd7a6c55`
**(No description)**
```python
<!-- ERROR reading f51b92e1d9cbbcf0aa3dc46b892c08fd7a6c55: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/7e/f59590c76ee75733d78b061d4108d49f209ee5`
**(No description)**
```python
<!-- ERROR reading f59590c76ee75733d78b061d4108d49f209ee5: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/7e/f9bcefdec05490393466f032548f24d41ea0b8`
**(No description)**
```python
<!-- ERROR reading f9bcefdec05490393466f032548f24d41ea0b8: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/10/4eebf5a3002fccdaceef3a4cb936173c1c2035`
**(No description)**
```python
<!-- ERROR reading 4eebf5a3002fccdaceef3a4cb936173c1c2035: 'utf-8' codec can't decode byte 0xdd in position 4: invalid continuation byte -->
```

### `.git/objects/10/7690266e16e85add5b7960e1915d153ceb8ccc`
**(No description)**
```python
<!-- ERROR reading 7690266e16e85add5b7960e1915d153ceb8ccc: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/10/c1b5607fa964ef247b60db9ff3c7d5aa1e09c7`
**(No description)**
```python
<!-- ERROR reading c1b5607fa964ef247b60db9ff3c7d5aa1e09c7: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/10/df115a7b9f975493476da763cc1e26dbd822e5`
**(No description)**
```python
<!-- ERROR reading df115a7b9f975493476da763cc1e26dbd822e5: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/10/ed362539718aed693f8155ce7ad55c64163aff`
**(No description)**
```python
<!-- ERROR reading ed362539718aed693f8155ce7ad55c64163aff: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/19/1e712dbddc442d18c8addbaf6fff74ad9055e7`
**(No description)**
```python
<!-- ERROR reading 1e712dbddc442d18c8addbaf6fff74ad9055e7: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/19/2205dfa5fda066e479ba073379747ae0abbba5`
**(No description)**
```python
<!-- ERROR reading 2205dfa5fda066e479ba073379747ae0abbba5: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/19/579c1a0fa38c088a7cbb80950d0c85f5514cca`
**(No description)**
```python
<!-- ERROR reading 579c1a0fa38c088a7cbb80950d0c85f5514cca: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/19/6a57546e7908425b6fcb43855c0b73d00a100f`
**(No description)**
```python
<!-- ERROR reading 6a57546e7908425b6fcb43855c0b73d00a100f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/19/72806e7163f96bfd1e439f0fc53fe85501af7d`
**(No description)**
```python
<!-- ERROR reading 72806e7163f96bfd1e439f0fc53fe85501af7d: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/19/9ba918d17a83e5a2fe8da6eda50ab2a1aace90`
**(No description)**
```python
<!-- ERROR reading 9ba918d17a83e5a2fe8da6eda50ab2a1aace90: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/19/a169fc30183db91f931ad6ad04fbc0e16559b3`
**(No description)**
```python
<!-- ERROR reading a169fc30183db91f931ad6ad04fbc0e16559b3: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/19/b0d9fa6dbcbe8f9b08a709419372c8f445bc23`
**(No description)**
```python
<!-- ERROR reading b0d9fa6dbcbe8f9b08a709419372c8f445bc23: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/19/b6b45242c16a1025465309eec2ca5009319de3`
**(No description)**
```python
<!-- ERROR reading b6b45242c16a1025465309eec2ca5009319de3: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/4c/379aa6f69ff56c8f19612002c6e3e939ea6012`
**(No description)**
```python
<!-- ERROR reading 379aa6f69ff56c8f19612002c6e3e939ea6012: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/4c/52d77bcaaa811202bfd5f20e16487ed6cd2cf8`
**(No description)**
```python
<!-- ERROR reading 52d77bcaaa811202bfd5f20e16487ed6cd2cf8: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/4c/58cdbdbe7ff605a215d3fd69e7d1fb4828264e`
**(No description)**
```python
<!-- ERROR reading 58cdbdbe7ff605a215d3fd69e7d1fb4828264e: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/4c/692a6e80da7644831e8c897950300d87341bc5`
**(No description)**
```python
<!-- ERROR reading 692a6e80da7644831e8c897950300d87341bc5: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/4c/7350fea9e5e59091a765ef3d2b979c688b07a8`
**(No description)**
```python
<!-- ERROR reading 7350fea9e5e59091a765ef3d2b979c688b07a8: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/4c/8911305680c1083b2da9b87ece12bc36f3a9e1`
**(No description)**
```python
<!-- ERROR reading 8911305680c1083b2da9b87ece12bc36f3a9e1: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/4c/996659c814f7488cf7e295995e4d6db93ea9ef`
**(No description)**
```python
<!-- ERROR reading 996659c814f7488cf7e295995e4d6db93ea9ef: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/4c/ae78838708b07f76357f938289fce8a200e98e`
**(No description)**
```python
<!-- ERROR reading ae78838708b07f76357f938289fce8a200e98e: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/4c/b24fe1a3c98d57564700a8724f793f453d93f8`
**(No description)**
```python
<!-- ERROR reading b24fe1a3c98d57564700a8724f793f453d93f8: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/4c/ba90eefe8ef9188a821acf880f51a7058e342b`
**(No description)**
```python
<!-- ERROR reading ba90eefe8ef9188a821acf880f51a7058e342b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/4c/c55741926b452344e99ee45b64f8a317806870`
**(No description)**
```python
<!-- ERROR reading c55741926b452344e99ee45b64f8a317806870: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/4c/de7a15f4e3739dae80d9b2b33fb89cf7be0be3`
**(No description)**
```python
<!-- ERROR reading de7a15f4e3739dae80d9b2b33fb89cf7be0be3: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/4c/fce8365f2195bd4cec4e867bac6f32a2a16e2c`
**(No description)**
```python
<!-- ERROR reading fce8365f2195bd4cec4e867bac6f32a2a16e2c: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/26/10d0e1422dd5021a7d5ff2e78992dece7cdc8f`
**(No description)**
```python
<!-- ERROR reading 10d0e1422dd5021a7d5ff2e78992dece7cdc8f: 'utf-8' codec can't decode byte 0x96 in position 3: invalid start byte -->
```

### `.git/objects/26/202f9760fc50044201b79076ea82f43b3941f8`
**(No description)**
```python
<!-- ERROR reading 202f9760fc50044201b79076ea82f43b3941f8: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/26/65e74bafceae8315eb920879ac78810ef10818`
**(No description)**
```python
<!-- ERROR reading 65e74bafceae8315eb920879ac78810ef10818: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/26/cfb440fa51d37c70c4d3ad9577ce285f69ce25`
**(No description)**
```python
<!-- ERROR reading cfb440fa51d37c70c4d3ad9577ce285f69ce25: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/26/d033b7867ba2b9d953256bdfe550e65c150370`
**(No description)**
```python
<!-- ERROR reading d033b7867ba2b9d953256bdfe550e65c150370: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/26/d70ecafeb95e9d48c202fa0b33248d7c3c8240`
**(No description)**
```python
<!-- ERROR reading d70ecafeb95e9d48c202fa0b33248d7c3c8240: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/21/6220149ddc458fa32be71f5629b07c3f1a73e0`
**(No description)**
```python
<!-- ERROR reading 6220149ddc458fa32be71f5629b07c3f1a73e0: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/21/634f588e512c8f2d62d26043bfe089471c171a`
**(No description)**
```python
<!-- ERROR reading 634f588e512c8f2d62d26043bfe089471c171a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/21/64db192b35849a93d661cb58a0285b123df995`
**(No description)**
```python
<!-- ERROR reading 64db192b35849a93d661cb58a0285b123df995: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/21/71abd6969f6823454d704c5eea3e278bbe8005`
**(No description)**
```python
<!-- ERROR reading 71abd6969f6823454d704c5eea3e278bbe8005: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/21/93e81945c2955a6b6559b3c91f758e6d137ccc`
**(No description)**
```python
<!-- ERROR reading 93e81945c2955a6b6559b3c91f758e6d137ccc: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/21/a3870b6be9a6a365037326c2085ff2715022cc`
**(No description)**
```python
<!-- ERROR reading a3870b6be9a6a365037326c2085ff2715022cc: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/21/aaa72961a8af71c17d2cb3b76d5f7f567100e4`
**(No description)**
```python
<!-- ERROR reading aaa72961a8af71c17d2cb3b76d5f7f567100e4: 'utf-8' codec can't decode byte 0xc9 in position 3: invalid continuation byte -->
```

### `.git/objects/21/da147793b735d2108b9d908ded7001a8ba8d32`
**(No description)**
```python
<!-- ERROR reading da147793b735d2108b9d908ded7001a8ba8d32: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/21/e4ab2285771f30ae33e93a05636040c16035d1`
**(No description)**
```python
<!-- ERROR reading e4ab2285771f30ae33e93a05636040c16035d1: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/4d/998578d7b5d39ae1cd5ce8832e7cd85ed2a1d1`
**(No description)**
```python
<!-- ERROR reading 998578d7b5d39ae1cd5ce8832e7cd85ed2a1d1: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/4d/c1af4af03f52131610c7c6313a93aef39b4748`
**(No description)**
```python
<!-- ERROR reading c1af4af03f52131610c7c6313a93aef39b4748: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/4d/d407c145fc359a49cc17ed3d6b7496411f6f36`
**(No description)**
```python
<!-- ERROR reading d407c145fc359a49cc17ed3d6b7496411f6f36: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/4d/f50af33f804651539767cc9f041aa21331908e`
**(No description)**
```python
<!-- ERROR reading f50af33f804651539767cc9f041aa21331908e: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/4d/f8f7ef1f3af721d62f0f3c556f6c48c6e54a8a`
**(No description)**
```python
<!-- ERROR reading f8f7ef1f3af721d62f0f3c556f6c48c6e54a8a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/75/4715a5084a9e4f04544ac8a4426d0871a0eb88`
**(No description)**
```python
<!-- ERROR reading 4715a5084a9e4f04544ac8a4426d0871a0eb88: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/75/5c3bc83a2df500cb9cef69cbeb6f4b7dc0d8a0`
**(No description)**
```python
<!-- ERROR reading 5c3bc83a2df500cb9cef69cbeb6f4b7dc0d8a0: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/75/9d9a56ba0102bb3b7b3abfcfae6731a2ecc243`
**(No description)**
```python
<!-- ERROR reading 9d9a56ba0102bb3b7b3abfcfae6731a2ecc243: 'utf-8' codec can't decode byte 0x93 in position 3: invalid start byte -->
```

### `.git/objects/75/e0057bbad50ca4c117b9130b92f1bed2720669`
**(No description)**
```python
<!-- ERROR reading e0057bbad50ca4c117b9130b92f1bed2720669: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/81/1ce89d566dea4fb4fa17a742b89a906496df76`
**(No description)**
```python
<!-- ERROR reading 1ce89d566dea4fb4fa17a742b89a906496df76: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/81/23a484e48e5b63593bf0a80bc68b394d28e64a`
**(No description)**
```python
<!-- ERROR reading 23a484e48e5b63593bf0a80bc68b394d28e64a: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/81/3baf37e21ad36ceac4f4b6b33067fe01609e0f`
**(No description)**
```python
<!-- ERROR reading 3baf37e21ad36ceac4f4b6b33067fe01609e0f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/81/3f85f5ed2c2bbf5340f24bea31ddf573c379a3`
**(No description)**
```python
<!-- ERROR reading 3f85f5ed2c2bbf5340f24bea31ddf573c379a3: 'utf-8' codec can't decode byte 0xb6 in position 9: invalid start byte -->
```

### `.git/objects/81/5650e81fe23c35523e66ff73e468ada1fd507d`
**(No description)**
```python
<!-- ERROR reading 5650e81fe23c35523e66ff73e468ada1fd507d: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/81/90f2bc66e66aa57096b8b077f86342d1d61f69`
**(No description)**
```python
<!-- ERROR reading 90f2bc66e66aa57096b8b077f86342d1d61f69: 'utf-8' codec can't decode byte 0xcd in position 19: invalid continuation byte -->
```

### `.git/objects/81/9fe1274d301432bf68c1554abe5c88e8624c1a`
**(No description)**
```python
<!-- ERROR reading 9fe1274d301432bf68c1554abe5c88e8624c1a: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/81/e89faefed9050e59177af5d91872355410e97a`
**(No description)**
```python
<!-- ERROR reading e89faefed9050e59177af5d91872355410e97a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/81/f74be52dc1b1b1870c3d7b3047f336afa50b42`
**(No description)**
```python
<!-- ERROR reading f74be52dc1b1b1870c3d7b3047f336afa50b42: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/86/0f259bd7e315c5b69f1ada19739b87eed0ecce`
**(No description)**
```python
<!-- ERROR reading 0f259bd7e315c5b69f1ada19739b87eed0ecce: 'utf-8' codec can't decode byte 0xb3 in position 5: invalid start byte -->
```

### `.git/objects/86/15a56b3609880ca754e02e739b8f4939be1e5d`
**(No description)**
```python
<!-- ERROR reading 15a56b3609880ca754e02e739b8f4939be1e5d: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/86/6620841057260527275870d99f1da5884321b6`
**(No description)**
```python
<!-- ERROR reading 6620841057260527275870d99f1da5884321b6: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/86/68b3b0ec1deec2aeb7ff6bd94265d6705e05bf`
**(No description)**
```python
<!-- ERROR reading 68b3b0ec1deec2aeb7ff6bd94265d6705e05bf: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/86/afa034745e5516ab15be0b37836a6a9e412c2a`
**(No description)**
```python
<!-- ERROR reading afa034745e5516ab15be0b37836a6a9e412c2a: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/86/c069a7c2afbd54954452fb3a417a842cbdd24f`
**(No description)**
```python
<!-- ERROR reading c069a7c2afbd54954452fb3a417a842cbdd24f: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/86/dad4a3a84d07d6860a11c334a375ec5f16047e`
**(No description)**
```python
<!-- ERROR reading dad4a3a84d07d6860a11c334a375ec5f16047e: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/86/dbdebdf00aa450591e296a8912697b7506ab59`
**(No description)**
```python
<!-- ERROR reading dbdebdf00aa450591e296a8912697b7506ab59: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/86/ea8c40da3264422a159353069cf0158a732f39`
**(No description)**
```python
<!-- ERROR reading ea8c40da3264422a159353069cf0158a732f39: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/72/1f411cfc44f6d24c13112e4246b5ad776a5e0b`
**(No description)**
```python
<!-- ERROR reading 1f411cfc44f6d24c13112e4246b5ad776a5e0b: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/72/79a5d066227dcfa3f2d199d9fa71d3c062d67a`
**(No description)**
```python
<!-- ERROR reading 79a5d066227dcfa3f2d199d9fa71d3c062d67a: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/72/aa5bfd4b60d8e6ef6ed0cf2ae4f763d12195cc`
**(No description)**
```python
<!-- ERROR reading aa5bfd4b60d8e6ef6ed0cf2ae4f763d12195cc: 'utf-8' codec can't decode byte 0xeb in position 4: invalid continuation byte -->
```

### `.git/objects/72/b9a3e424707633c7e31a347170f358cfa3f87a`
**(No description)**
```python
<!-- ERROR reading b9a3e424707633c7e31a347170f358cfa3f87a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/72/bc89d91a4e7c2400511e280c26dd1cb2fc6502`
**(No description)**
```python
<!-- ERROR reading bc89d91a4e7c2400511e280c26dd1cb2fc6502: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/44/1b543f4ea46735ff8b75f211970739c81974ea`
**(No description)**
```python
<!-- ERROR reading 1b543f4ea46735ff8b75f211970739c81974ea: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/44/35a02f3e1be52b7505fbde16e147a6c21cd72e`
**(No description)**
```python
<!-- ERROR reading 35a02f3e1be52b7505fbde16e147a6c21cd72e: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/44/5bd260380b6c727806cfc288dfc77567c148f4`
**(No description)**
```python
<!-- ERROR reading 5bd260380b6c727806cfc288dfc77567c148f4: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/44/939e1c6d40539eb8173bf1527db926c5a54658`
**(No description)**
```python
<!-- ERROR reading 939e1c6d40539eb8173bf1527db926c5a54658: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/44/d4ada86d7e453df892db115b4acd1c7a95e603`
**(No description)**
```python
<!-- ERROR reading d4ada86d7e453df892db115b4acd1c7a95e603: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/44/dd9bdc3039122cc98014c1439ca254313fd014`
**(No description)**
```python
<!-- ERROR reading dd9bdc3039122cc98014c1439ca254313fd014: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/44/ee41e0167da6fdb8ace91004f7af4f0e48e904`
**(No description)**
```python
<!-- ERROR reading ee41e0167da6fdb8ace91004f7af4f0e48e904: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/2a/12b8865c9f30d58aa839c4b529d6476e1c8e6e`
**(No description)**
```python
<!-- ERROR reading 12b8865c9f30d58aa839c4b529d6476e1c8e6e: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/2a/59337e524c7eee2b4e92e2499fb3d2d7979bef`
**(No description)**
```python
<!-- ERROR reading 59337e524c7eee2b4e92e2499fb3d2d7979bef: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/2a/62db8818d2db308341d10384078321bf3b6eb3`
**(No description)**
```python
<!-- ERROR reading 62db8818d2db308341d10384078321bf3b6eb3: 'utf-8' codec can't decode byte 0xcd in position 4: invalid continuation byte -->
```

### `.git/objects/2a/92e62b7b2e8dab77cbe0c2dbb79c810af7f452`
**(No description)**
```python
<!-- ERROR reading 92e62b7b2e8dab77cbe0c2dbb79c810af7f452: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/2a/bdefedabe1e7a2d0c583211809c9ea7a049470`
**(No description)**
```python
<!-- ERROR reading bdefedabe1e7a2d0c583211809c9ea7a049470: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/2f/251df6036953e1fb211744c75ac463ca2e893c`
**(No description)**
```python
<!-- ERROR reading 251df6036953e1fb211744c75ac463ca2e893c: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/2f/68fc8600038d8de10017b0d02a3fde77a06ba6`
**(No description)**
```python
<!-- ERROR reading 68fc8600038d8de10017b0d02a3fde77a06ba6: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/2f/9898a8f930247a3d0cd3e26d3e25f831bb1f92`
**(No description)**
```python
<!-- ERROR reading 9898a8f930247a3d0cd3e26d3e25f831bb1f92: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/2f/b3852c3cf1a565ccf813f876a135ecf6f99712`
**(No description)**
```python
<!-- ERROR reading b3852c3cf1a565ccf813f876a135ecf6f99712: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/43/0d0668727cd0521270a52c962867907d743b34`
**(No description)**
```python
<!-- ERROR reading 0d0668727cd0521270a52c962867907d743b34: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/43/1d75a6406f3cf79ae4fcd26a2ad35fb5030526`
**(No description)**
```python
<!-- ERROR reading 1d75a6406f3cf79ae4fcd26a2ad35fb5030526: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/43/55a63235c7b6d8a9b8389c3fc203b9b3529a36`
**(No description)**
```python
<!-- ERROR reading 55a63235c7b6d8a9b8389c3fc203b9b3529a36: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/43/7a43696b84e7475f9aa23d25c014310dd2625a`
**(No description)**
```python
<!-- ERROR reading 7a43696b84e7475f9aa23d25c014310dd2625a: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/43/bd29524936ce2017866e8e8a56de5dbc6dbfd7`
**(No description)**
```python
<!-- ERROR reading bd29524936ce2017866e8e8a56de5dbc6dbfd7: 'utf-8' codec can't decode byte 0xfc in position 10: invalid start byte -->
```

### `.git/objects/43/cce1e4b8da900928a0da78c6dfcad7aa7eef50`
**(No description)**
```python
<!-- ERROR reading cce1e4b8da900928a0da78c6dfcad7aa7eef50: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/43/f4230aead2fd8c9f685bd0a726cf0723a9d98d`
**(No description)**
```python
<!-- ERROR reading f4230aead2fd8c9f685bd0a726cf0723a9d98d: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/88/19efda65b9f6bf1315ad15bedc5a3857bf67fc`
**(No description)**
```python
<!-- ERROR reading 19efda65b9f6bf1315ad15bedc5a3857bf67fc: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/88/2c635a86966668f9c8783b996bf00104bf4838`
**(No description)**
```python
<!-- ERROR reading 2c635a86966668f9c8783b996bf00104bf4838: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/88/dc7f01e132933728cbcf45c88ce82e85ddf65f`
**(No description)**
```python
<!-- ERROR reading dc7f01e132933728cbcf45c88ce82e85ddf65f: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/9f/0ad778b51c9e8f4188797ef5c578ec418f9302`
**(No description)**
```python
<!-- ERROR reading 0ad778b51c9e8f4188797ef5c578ec418f9302: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/9f/2510c03429b6de24063bec5937e4334077722d`
**(No description)**
```python
<!-- ERROR reading 2510c03429b6de24063bec5937e4334077722d: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/9f/35bae568e33e6a9e1219761c83cc8350fa0532`
**(No description)**
```python
<!-- ERROR reading 35bae568e33e6a9e1219761c83cc8350fa0532: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/9f/aa49f0a6775942a742da64b8542dbca030d78f`
**(No description)**
```python
<!-- ERROR reading aa49f0a6775942a742da64b8542dbca030d78f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/9f/dc123ced9c64182262ea5f9156a4b789910e1b`
**(No description)**
```python
<!-- ERROR reading dc123ced9c64182262ea5f9156a4b789910e1b: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/9f/e1c591f8704c4c8ac66b050ea29fb377e1a6fe`
**(No description)**
```python
<!-- ERROR reading e1c591f8704c4c8ac66b050ea29fb377e1a6fe: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/6b/01aac9209fdcc893f4b24fd09d8a3f14149ec9`
**(No description)**
```python
<!-- ERROR reading 01aac9209fdcc893f4b24fd09d8a3f14149ec9: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6b/1f8b6db1ee001e80415c8abdb7007ba028dfe3`
**(No description)**
```python
<!-- ERROR reading 1f8b6db1ee001e80415c8abdb7007ba028dfe3: 'utf-8' codec can't decode byte 0x8a in position 20: invalid start byte -->
```

### `.git/objects/6b/20df315b23ecd1e3d0ec32c11c0b5ced577efe`
**(No description)**
```python
<!-- ERROR reading 20df315b23ecd1e3d0ec32c11c0b5ced577efe: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/6b/24965b8029f7b384be4e9ec3dbc12abe17df72`
**(No description)**
```python
<!-- ERROR reading 24965b8029f7b384be4e9ec3dbc12abe17df72: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/6b/2863e4e5518786305942c08923055c13b7504b`
**(No description)**
```python
<!-- ERROR reading 2863e4e5518786305942c08923055c13b7504b: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/6b/46f4eaef63a97d9263f0add4da1ac657b86ced`
**(No description)**
```python
<!-- ERROR reading 46f4eaef63a97d9263f0add4da1ac657b86ced: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6b/71975f08587ca8861acc2380f17701b7c7c656`
**(No description)**
```python
<!-- ERROR reading 71975f08587ca8861acc2380f17701b7c7c656: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/6b/882fa3515b66fe40dbcb0b4d140209a3291c5a`
**(No description)**
```python
<!-- ERROR reading 882fa3515b66fe40dbcb0b4d140209a3291c5a: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/07/03564993e3bccb797a79968d19f45eef3cebff`
**(No description)**
```python
<!-- ERROR reading 03564993e3bccb797a79968d19f45eef3cebff: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/07/0e77c88e54021f2be1c34df90d97f80f19d3d1`
**(No description)**
```python
<!-- ERROR reading 0e77c88e54021f2be1c34df90d97f80f19d3d1: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/07/16871caabdbbb3e77a0371d49936cef1923ea1`
**(No description)**
```python
<!-- ERROR reading 16871caabdbbb3e77a0371d49936cef1923ea1: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/07/1fea5d038cb0425a962a8b6bea55a9c158dd5d`
**(No description)**
```python
<!-- ERROR reading 1fea5d038cb0425a962a8b6bea55a9c158dd5d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/07/2d19661ae0a97cbed5a90f690f2e107870c56b`
**(No description)**
```python
<!-- ERROR reading 2d19661ae0a97cbed5a90f690f2e107870c56b: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/07/5bf8a469d44d2388b08ec3d009fe55d44cb6eb`
**(No description)**
```python
<!-- ERROR reading 5bf8a469d44d2388b08ec3d009fe55d44cb6eb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/07/6b4a0e8a2723f875588a06bfd6f861d725be99`
**(No description)**
```python
<!-- ERROR reading 6b4a0e8a2723f875588a06bfd6f861d725be99: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/07/bad5d31c1ec7aa7ac081dac5586db91f3c5a99`
**(No description)**
```python
<!-- ERROR reading bad5d31c1ec7aa7ac081dac5586db91f3c5a99: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/07/d0f09bac38f7deca2514e7e33c177577e8102f`
**(No description)**
```python
<!-- ERROR reading d0f09bac38f7deca2514e7e33c177577e8102f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/07/ed348a4b5918c9d2b8a4a32f7734901c35b4ab`
**(No description)**
```python
<!-- ERROR reading ed348a4b5918c9d2b8a4a32f7734901c35b4ab: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/38/3063e45c643ee7f5feeed2028c45c0f8bd3c40`
**(No description)**
```python
<!-- ERROR reading 3063e45c643ee7f5feeed2028c45c0f8bd3c40: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/38/3aa5900e497b9494b4534b350631569e33d05b`
**(No description)**
```python
<!-- ERROR reading 3aa5900e497b9494b4534b350631569e33d05b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/38/4dea976adad1c3d6004888078dd0fe00b4c268`
**(No description)**
```python
<!-- ERROR reading 4dea976adad1c3d6004888078dd0fe00b4c268: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/38/579529aa15f3ea4f1afad7d25190fbc1318266`
**(No description)**
```python
<!-- ERROR reading 579529aa15f3ea4f1afad7d25190fbc1318266: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/38/5faab0525ccdbfd1070a8bebcca3ac8617236e`
**(No description)**
```python
<!-- ERROR reading 5faab0525ccdbfd1070a8bebcca3ac8617236e: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/38/693f4fc6e33766f7a6b4f1227867ae86d2da32`
**(No description)**
```python
<!-- ERROR reading 693f4fc6e33766f7a6b4f1227867ae86d2da32: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/38/83fdd9c9069c3655321da77d16499506b49958`
**(No description)**
```python
<!-- ERROR reading 83fdd9c9069c3655321da77d16499506b49958: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/38/9c73c0835645acd8db3322cc2b2290df016611`
**(No description)**
```python
<!-- ERROR reading 9c73c0835645acd8db3322cc2b2290df016611: 'utf-8' codec can't decode byte 0xaa in position 6: invalid start byte -->
```

### `.git/objects/38/b961d10de88bebc98c758d0d1f14af1e7c0370`
**(No description)**
```python
<!-- ERROR reading b961d10de88bebc98c758d0d1f14af1e7c0370: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/38/e9ccbf7df923f4f68195b4a2079e4228e6ee04`
**(No description)**
```python
<!-- ERROR reading e9ccbf7df923f4f68195b4a2079e4228e6ee04: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/38/f32517aa8f6cf5970f7ceddd1a415289184c3e`
**(No description)**
```python
<!-- ERROR reading f32517aa8f6cf5970f7ceddd1a415289184c3e: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/00/2b60cde1bf28bbbf20af824638503d598fbc60`
**(No description)**
```python
<!-- ERROR reading 2b60cde1bf28bbbf20af824638503d598fbc60: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/00/337dd1898b1152673fe0a6f2c11c8806df126a`
**(No description)**
```python
<!-- ERROR reading 337dd1898b1152673fe0a6f2c11c8806df126a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/00/371e86a87edfc5f8d1d1352360bfae0cce8e65`
**(No description)**
```python
<!-- ERROR reading 371e86a87edfc5f8d1d1352360bfae0cce8e65: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/00/376349e69ad8b9dbf401cddc34055951e4b02e`
**(No description)**
```python
<!-- ERROR reading 376349e69ad8b9dbf401cddc34055951e4b02e: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/00/69523a04969dd920ea4b43a497162157729174`
**(No description)**
```python
<!-- ERROR reading 69523a04969dd920ea4b43a497162157729174: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/00/a70b02dc3928bd0ca214548032478d219ffb69`
**(No description)**
```python
<!-- ERROR reading a70b02dc3928bd0ca214548032478d219ffb69: 'utf-8' codec can't decode byte 0xdc in position 6: invalid continuation byte -->
```

### `.git/objects/00/addc2725a66c965dbefacd3692ecbbc52a80d8`
**(No description)**
```python
<!-- ERROR reading addc2725a66c965dbefacd3692ecbbc52a80d8: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/6e/0a3fae6c176485e506b498200ac22c499c6c50`
**(No description)**
```python
<!-- ERROR reading 0a3fae6c176485e506b498200ac22c499c6c50: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/6e/1c89f1f235b29809bfacb6df2cf00f2215a47f`
**(No description)**
```python
<!-- ERROR reading 1c89f1f235b29809bfacb6df2cf00f2215a47f: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/6e/33c8a39f2c6e9768760cc25f06e6c4c87ac42a`
**(No description)**
```python
<!-- ERROR reading 33c8a39f2c6e9768760cc25f06e6c4c87ac42a: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/6e/3f15c557c911e020a386ad700c815932bd375d`
**(No description)**
```python
<!-- ERROR reading 3f15c557c911e020a386ad700c815932bd375d: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/6e/47b8732d1c32ff782c893c1436d34a816554ae`
**(No description)**
```python
<!-- ERROR reading 47b8732d1c32ff782c893c1436d34a816554ae: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/6e/8644258a6ccf999a19f69c359452a109e54ffe`
**(No description)**
```python
<!-- ERROR reading 8644258a6ccf999a19f69c359452a109e54ffe: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/6e/874dd12c61df0c69b12de40e5122fce2738495`
**(No description)**
```python
<!-- ERROR reading 874dd12c61df0c69b12de40e5122fce2738495: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/6e/d97a7bcdc0d0d0e13f5e9a5a38996a24a3b642`
**(No description)**
```python
<!-- ERROR reading d97a7bcdc0d0d0e13f5e9a5a38996a24a3b642: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/9a/37db573881e426acc756db236be0eb052ef0d9`
**(No description)**
```python
<!-- ERROR reading 37db573881e426acc756db236be0eb052ef0d9: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/9a/42d586fd71a786ba63a4d5ce55a0ed93d866b0`
**(No description)**
```python
<!-- ERROR reading 42d586fd71a786ba63a4d5ce55a0ed93d866b0: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/9a/69f2b39390cd1221f96b644b8d494597ce205c`
**(No description)**
```python
<!-- ERROR reading 69f2b39390cd1221f96b644b8d494597ce205c: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/9a/7957ffbafcfa482c34b063eb5f1698bed33a3e`
**(No description)**
```python
<!-- ERROR reading 7957ffbafcfa482c34b063eb5f1698bed33a3e: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/9a/89a838b9a5cb264e9ae9d269fbedca6e2d6333`
**(No description)**
```python
<!-- ERROR reading 89a838b9a5cb264e9ae9d269fbedca6e2d6333: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/9a/8dafba3079c6b8a85d9700ec98b96b4d612dea`
**(No description)**
```python
<!-- ERROR reading 8dafba3079c6b8a85d9700ec98b96b4d612dea: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/9a/b2df3c98e1e08a920de9439e78ecd65c2daada`
**(No description)**
```python
<!-- ERROR reading b2df3c98e1e08a920de9439e78ecd65c2daada: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/9a/d3527b94ce034bb3967b3bf0969403118d4284`
**(No description)**
```python
<!-- ERROR reading d3527b94ce034bb3967b3bf0969403118d4284: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/9a/f3dad0032c43bcfdcf1e5f5089ca78c6a4c50e`
**(No description)**
```python
<!-- ERROR reading f3dad0032c43bcfdcf1e5f5089ca78c6a4c50e: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/36/1583bede6b2b84088b38054d5d8116ef9f1597`
**(No description)**
```python
<!-- ERROR reading 1583bede6b2b84088b38054d5d8116ef9f1597: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/36/17901553783727572aad586872a3b2c010359d`
**(No description)**
```python
<!-- ERROR reading 17901553783727572aad586872a3b2c010359d: 'utf-8' codec can't decode byte 0x88 in position 17: invalid start byte -->
```

### `.git/objects/36/2030584fcc81bbbdb9be82156ab0adb1119609`
**(No description)**
```python
<!-- ERROR reading 2030584fcc81bbbdb9be82156ab0adb1119609: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/36/2d791823ee675fbd7092edba74e393372837e4`
**(No description)**
```python
<!-- ERROR reading 2d791823ee675fbd7092edba74e393372837e4: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/36/3f8be819d2576ea65365e625dd1596ea40429a`
**(No description)**
```python
<!-- ERROR reading 3f8be819d2576ea65365e625dd1596ea40429a: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/36/51c43182a0b32f676983e781129b7f660d112b`
**(No description)**
```python
<!-- ERROR reading 51c43182a0b32f676983e781129b7f660d112b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/36/64cee86c4b172b5bee6997a0b94e5291e5b66b`
**(No description)**
```python
<!-- ERROR reading 64cee86c4b172b5bee6997a0b94e5291e5b66b: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/36/66ab04ca6460be9bc6944c0f045be7ff44c365`
**(No description)**
```python
<!-- ERROR reading 66ab04ca6460be9bc6944c0f045be7ff44c365: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/36/6d1a7e4f2651984c09a4c304afb9c0be06627c`
**(No description)**
```python
<!-- ERROR reading 6d1a7e4f2651984c09a4c304afb9c0be06627c: 'utf-8' codec can't decode byte 0xec in position 9: invalid continuation byte -->
```

### `.git/objects/36/718e88e5c64e1927dfe5d89afd54edd62fda3c`
**(No description)**
```python
<!-- ERROR reading 718e88e5c64e1927dfe5d89afd54edd62fda3c: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/36/c9252c647e67bc7353c523152568b993c1331f`
**(No description)**
```python
<!-- ERROR reading c9252c647e67bc7353c523152568b993c1331f: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/36/ce16806219d4bdf9c628a70ce581b9b5208c9e`
**(No description)**
```python
<!-- ERROR reading ce16806219d4bdf9c628a70ce581b9b5208c9e: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/36/d9b306c992b83a8033c0ee66daa141d23d010c`
**(No description)**
```python
<!-- ERROR reading d9b306c992b83a8033c0ee66daa141d23d010c: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/5c/00fc3ff373e42f95c8c44b1ac7e8e85c311bae`
**(No description)**
```python
<!-- ERROR reading 00fc3ff373e42f95c8c44b1ac7e8e85c311bae: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/5c/0a76b0058d4497b1468c72b78fec088963c9b8`
**(No description)**
```python
<!-- ERROR reading 0a76b0058d4497b1468c72b78fec088963c9b8: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/5c/3122bfab194fa65e2956a985eb934476ffbd52`
**(No description)**
```python
<!-- ERROR reading 3122bfab194fa65e2956a985eb934476ffbd52: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/5c/5f6af86538b6343042fd683cb094c70f595d5c`
**(No description)**
```python
<!-- ERROR reading 5f6af86538b6343042fd683cb094c70f595d5c: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/5c/65ee2f5490d5d014fdc629cb52d52f646bcd2f`
**(No description)**
```python
<!-- ERROR reading 65ee2f5490d5d014fdc629cb52d52f646bcd2f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/5c/661e66c1fa1c66721b3a330a5bc583937d08c9`
**(No description)**
```python
<!-- ERROR reading 661e66c1fa1c66721b3a330a5bc583937d08c9: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/5c/b92e63a01796b1e5456c957f48f2d08631b653`
**(No description)**
```python
<!-- ERROR reading b92e63a01796b1e5456c957f48f2d08631b653: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/09/1450eb61c908dcd7d8441a0b29afbd752f7109`
**(No description)**
```python
<!-- ERROR reading 1450eb61c908dcd7d8441a0b29afbd752f7109: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/09/34f4eaf144035330f565464b89411da235a172`
**(No description)**
```python
<!-- ERROR reading 34f4eaf144035330f565464b89411da235a172: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/09/4cf1b4a97378c669f3440566e532fa8ef4535c`
**(No description)**
```python
<!-- ERROR reading 4cf1b4a97378c669f3440566e532fa8ef4535c: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/09/b091a6c94820e8cb4258fb862937220c2c5feb`
**(No description)**
```python
<!-- ERROR reading b091a6c94820e8cb4258fb862937220c2c5feb: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte -->
```

### `.git/objects/09/df984ea1b184c0af9666c98d0709364de024c5`
**(No description)**
```python
<!-- ERROR reading df984ea1b184c0af9666c98d0709364de024c5: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/5d/50c7d7e20c8b390edc0e6a2c362161641117d4`
**(No description)**
```python
<!-- ERROR reading 50c7d7e20c8b390edc0e6a2c362161641117d4: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/5d/510db868fb46c2af5896281920a95a498c16b5`
**(No description)**
```python
<!-- ERROR reading 510db868fb46c2af5896281920a95a498c16b5: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/5d/badfec967021e4865466c119fb638664f81a73`
**(No description)**
```python
<!-- ERROR reading badfec967021e4865466c119fb638664f81a73: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/5d/d1ab6da18ef67ae45007b5ace3440264dd0d5a`
**(No description)**
```python
<!-- ERROR reading d1ab6da18ef67ae45007b5ace3440264dd0d5a: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/5d/d6fdaf4182be93ba9891dec8be54ef0e201bcb`
**(No description)**
```python
<!-- ERROR reading d6fdaf4182be93ba9891dec8be54ef0e201bcb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/31/1b2b56c53f678ab95fc0def708c675d521a807`
**(No description)**
```python
<!-- ERROR reading 1b2b56c53f678ab95fc0def708c675d521a807: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/31/7098b8b59d7310bfbedf6c7f2e52a20045df47`
**(No description)**
```python
<!-- ERROR reading 7098b8b59d7310bfbedf6c7f2e52a20045df47: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/31/a1130ee549371dffc668e515d2ae5d91799aac`
**(No description)**
```python
<!-- ERROR reading a1130ee549371dffc668e515d2ae5d91799aac: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/31/f6d136c227b0c5aeb3276c3fd9f76a7927cc61`
**(No description)**
```python
<!-- ERROR reading f6d136c227b0c5aeb3276c3fd9f76a7927cc61: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/91/15f123f0274832af5ba1cf3c5481cc5353eecd`
**(No description)**
```python
<!-- ERROR reading 15f123f0274832af5ba1cf3c5481cc5353eecd: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/91/25ab32e5348b6e873c4b1939a887ebde35d97a`
**(No description)**
```python
<!-- ERROR reading 25ab32e5348b6e873c4b1939a887ebde35d97a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/91/3abfd6a23ce547f84de2adc41221012f1007d6`
**(No description)**
```python
<!-- ERROR reading 3abfd6a23ce547f84de2adc41221012f1007d6: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/91/53d150ce67a708f920fcf9c606970fc061f816`
**(No description)**
```python
<!-- ERROR reading 53d150ce67a708f920fcf9c606970fc061f816: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/91/58f968d630e9ad441e8b44049fee75cba2b795`
**(No description)**
```python
<!-- ERROR reading 58f968d630e9ad441e8b44049fee75cba2b795: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/91/7afbbcb6482ef01406aeaa1ed621f26f531a16`
**(No description)**
```python
<!-- ERROR reading 7afbbcb6482ef01406aeaa1ed621f26f531a16: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/91/f538bb1fd2ce62632e475053dc000e7833d11b`
**(No description)**
```python
<!-- ERROR reading f538bb1fd2ce62632e475053dc000e7833d11b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/65/35e163b1d4007c93aad278ee9963afa010d098`
**(No description)**
```python
<!-- ERROR reading 35e163b1d4007c93aad278ee9963afa010d098: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/65/4fa25ee9811c34039336b155ea0f895ef01668`
**(No description)**
```python
<!-- ERROR reading 4fa25ee9811c34039336b155ea0f895ef01668: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/65/ada12d12ada873baaae31fe12660e7fb3883fd`
**(No description)**
```python
<!-- ERROR reading ada12d12ada873baaae31fe12660e7fb3883fd: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/65/da0d8dc7f8cacd226c8b917bc7b849675d7143`
**(No description)**
```python
<!-- ERROR reading da0d8dc7f8cacd226c8b917bc7b849675d7143: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/62/0296d5ad6ca2cc49eb5d0dc140bcbc3204e9b4`
**(No description)**
```python
<!-- ERROR reading 0296d5ad6ca2cc49eb5d0dc140bcbc3204e9b4: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/62/2481e39f47ed19aaecf68fe71e34915d962a7b`
**(No description)**
```python
<!-- ERROR reading 2481e39f47ed19aaecf68fe71e34915d962a7b: 'utf-8' codec can't decode byte 0x8a in position 20: invalid start byte -->
```

### `.git/objects/62/56ecfd1e2c9ac4cfa3fac359cd12dce85b759c`
**(No description)**
```python
<!-- ERROR reading 56ecfd1e2c9ac4cfa3fac359cd12dce85b759c: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/62/961154f643da5fa22484b7bd1a8241c915c1da`
**(No description)**
```python
<!-- ERROR reading 961154f643da5fa22484b7bd1a8241c915c1da: 'utf-8' codec can't decode byte 0x85 in position 14: invalid start byte -->
```

### `.git/objects/62/9bf5de3f9c1b23c8034dd7d6b3360ea4c7e060`
**(No description)**
```python
<!-- ERROR reading 9bf5de3f9c1b23c8034dd7d6b3360ea4c7e060: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/62/b076cdee58ec8f34034141ba0befd9015b0c7e`
**(No description)**
```python
<!-- ERROR reading b076cdee58ec8f34034141ba0befd9015b0c7e: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/62/f0128453e7bc7ed7b64b3c57714d13daebd326`
**(No description)**
```python
<!-- ERROR reading f0128453e7bc7ed7b64b3c57714d13daebd326: 'utf-8' codec can't decode byte 0xc8 in position 17: invalid continuation byte -->
```

### `.git/objects/96/07211ee83c08cff2e09144aec43ca59afdb87c`
**(No description)**
```python
<!-- ERROR reading 07211ee83c08cff2e09144aec43ca59afdb87c: 'utf-8' codec can't decode byte 0xcf in position 23: invalid continuation byte -->
```

### `.git/objects/96/09f72c5417b635743be3f8ec1ff1e507665f2e`
**(No description)**
```python
<!-- ERROR reading 09f72c5417b635743be3f8ec1ff1e507665f2e: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/96/3eac530b9bc28d704d1bc410299c68e3216d4d`
**(No description)**
```python
<!-- ERROR reading 3eac530b9bc28d704d1bc410299c68e3216d4d: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/96/5e0b425a4da2d0eff10357630b8fccbf7899d0`
**(No description)**
```python
<!-- ERROR reading 5e0b425a4da2d0eff10357630b8fccbf7899d0: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/96/5fce29d3b9e01e9e9374a3d6318badeca7e1e1`
**(No description)**
```python
<!-- ERROR reading 5fce29d3b9e01e9e9374a3d6318badeca7e1e1: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/96/8e84fb401e7e0b730b3a7eaa5534d4db56cfdf`
**(No description)**
```python
<!-- ERROR reading 8e84fb401e7e0b730b3a7eaa5534d4db56cfdf: 'utf-8' codec can't decode byte 0xb7 in position 8: invalid start byte -->
```

### `.git/objects/96/a10d5380a2878f74e01c394e5b910e689f011c`
**(No description)**
```python
<!-- ERROR reading a10d5380a2878f74e01c394e5b910e689f011c: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/96/e2fc65a816432247eed7c83c86fc7458af1ed4`
**(No description)**
```python
<!-- ERROR reading e2fc65a816432247eed7c83c86fc7458af1ed4: 'utf-8' codec can't decode byte 0xb3 in position 5: invalid start byte -->
```

### `.git/objects/96/e973d0ce223f6bed9be9e6a6a2f3c01622c611`
**(No description)**
```python
<!-- ERROR reading e973d0ce223f6bed9be9e6a6a2f3c01622c611: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/3a/2cb59a6c1a55dd039fda04e0a82f5008eae3df`
**(No description)**
```python
<!-- ERROR reading 2cb59a6c1a55dd039fda04e0a82f5008eae3df: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/3a/31a285bf64816fba65d2cb76b7aea66abaf534`
**(No description)**
```python
<!-- ERROR reading 31a285bf64816fba65d2cb76b7aea66abaf534: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/3a/5bb9c885f38e7f2b3a9d3ea8583b19880525d9`
**(No description)**
```python
<!-- ERROR reading 5bb9c885f38e7f2b3a9d3ea8583b19880525d9: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/3a/82da9a939ee137122cbe71a78c403cbc5ca727`
**(No description)**
```python
<!-- ERROR reading 82da9a939ee137122cbe71a78c403cbc5ca727: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/3a/8ef46a3b22574c64fbed725c17c3bf2bf78c4b`
**(No description)**
```python
<!-- ERROR reading 8ef46a3b22574c64fbed725c17c3bf2bf78c4b: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/3a/a6bf21e44f3069adb94242fbba5c8160532a1c`
**(No description)**
```python
<!-- ERROR reading a6bf21e44f3069adb94242fbba5c8160532a1c: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/3a/c05cfd1077ba5664e98ecd1342f7c54360b936`
**(No description)**
```python
<!-- ERROR reading c05cfd1077ba5664e98ecd1342f7c54360b936: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/3a/d917222a4e5bb93fe1c9e8fe1713bcab3630b6`
**(No description)**
```python
<!-- ERROR reading d917222a4e5bb93fe1c9e8fe1713bcab3630b6: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/54/0e7a4dc79d02a820e291b57c43335d5aa25a41`
**(No description)**
```python
<!-- ERROR reading 0e7a4dc79d02a820e291b57c43335d5aa25a41: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/54/6abf741c6833e9371ccf2db38ec92f50efbe1e`
**(No description)**
```python
<!-- ERROR reading 6abf741c6833e9371ccf2db38ec92f50efbe1e: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/54/a03f6246efab2cb98a9b5108d17c099093fb14`
**(No description)**
```python
<!-- ERROR reading a03f6246efab2cb98a9b5108d17c099093fb14: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/54/c1fb7d0df128bfe16fb4cb03cdf23b8225af94`
**(No description)**
```python
<!-- ERROR reading c1fb7d0df128bfe16fb4cb03cdf23b8225af94: 'utf-8' codec can't decode byte 0xc9 in position 4: invalid continuation byte -->
```

### `.git/objects/98/0dfd23eedec7aaa03f5d98e4ee9ae82ad80baf`
**(No description)**
```python
<!-- ERROR reading 0dfd23eedec7aaa03f5d98e4ee9ae82ad80baf: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/98/1810ca1412ac2bac2e840dbff120002b56fba0`
**(No description)**
```python
<!-- ERROR reading 1810ca1412ac2bac2e840dbff120002b56fba0: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/98/18a8d1a9815eb3b847331d18c9c920e86e9188`
**(No description)**
```python
<!-- ERROR reading 18a8d1a9815eb3b847331d18c9c920e86e9188: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/98/18be2ab032617986b6bb9b6f9bf1bcbbc92641`
**(No description)**
```python
<!-- ERROR reading 18be2ab032617986b6bb9b6f9bf1bcbbc92641: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/98/1d2fcaef87c2d3fadb54c83afeb88ccdbaf561`
**(No description)**
```python
<!-- ERROR reading 1d2fcaef87c2d3fadb54c83afeb88ccdbaf561: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/98/34e11092ccbc3a04de706bd90cf6bc62d82c27`
**(No description)**
```python
<!-- ERROR reading 34e11092ccbc3a04de706bd90cf6bc62d82c27: 'utf-8' codec can't decode byte 0xb1 in position 4: invalid start byte -->
```

### `.git/objects/98/4100e71ea269cca3f77487f38103e5869fc278`
**(No description)**
```python
<!-- ERROR reading 4100e71ea269cca3f77487f38103e5869fc278: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/98/6ac57c2a23f07a9bbbd8f5071ec2f396c25f48`
**(No description)**
```python
<!-- ERROR reading 6ac57c2a23f07a9bbbd8f5071ec2f396c25f48: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/98/9e92c3458681a6f0be72ae4105ea742750d328`
**(No description)**
```python
<!-- ERROR reading 9e92c3458681a6f0be72ae4105ea742750d328: 'utf-8' codec can't decode byte 0xda in position 6: invalid continuation byte -->
```

### `.git/objects/98/b64b86e89a1b2b3233add2f1de0eed37ee10a2`
**(No description)**
```python
<!-- ERROR reading b64b86e89a1b2b3233add2f1de0eed37ee10a2: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/98/c0d20b7a64f4f998d7913e1d38a05dba20916c`
**(No description)**
```python
<!-- ERROR reading c0d20b7a64f4f998d7913e1d38a05dba20916c: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/98/f9970122088c14a5830e091ca8a12fc8e4c563`
**(No description)**
```python
<!-- ERROR reading f9970122088c14a5830e091ca8a12fc8e4c563: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/53/0abe75e0c00cbfcb2a310d872866f320977d0a`
**(No description)**
```python
<!-- ERROR reading 0abe75e0c00cbfcb2a310d872866f320977d0a: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/53/232d156ba65d137c5e087424ab5c53402bc35d`
**(No description)**
```python
<!-- ERROR reading 232d156ba65d137c5e087424ab5c53402bc35d: 'utf-8' codec can't decode byte 0xaa in position 6: invalid start byte -->
```

### `.git/objects/53/419f21a7bfe7668a30537f429d100a6add05ea`
**(No description)**
```python
<!-- ERROR reading 419f21a7bfe7668a30537f429d100a6add05ea: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/53/a0a09e0e9e28e3ae1588f163ef468b5fa2011c`
**(No description)**
```python
<!-- ERROR reading a0a09e0e9e28e3ae1588f163ef468b5fa2011c: 'utf-8' codec can't decode byte 0xb5 in position 8: invalid start byte -->
```

### `.git/objects/53/d52649e7620965ed194240a3becaa3ce3e3448`
**(No description)**
```python
<!-- ERROR reading d52649e7620965ed194240a3becaa3ce3e3448: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/3f/1070d08f3ac5bd554794401734eb349373ab8e`
**(No description)**
```python
<!-- ERROR reading 1070d08f3ac5bd554794401734eb349373ab8e: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/3f/4d300cef077e698989245562375a9444d983fa`
**(No description)**
```python
<!-- ERROR reading 4d300cef077e698989245562375a9444d983fa: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/3f/6a3f4183101bfbb198505c3c25806d77680e4b`
**(No description)**
```python
<!-- ERROR reading 6a3f4183101bfbb198505c3c25806d77680e4b: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/3f/7520ee4ad557e4d228a501daa3cae8818b8ae7`
**(No description)**
```python
<!-- ERROR reading 7520ee4ad557e4d228a501daa3cae8818b8ae7: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/3f/83ef0f533b21b6e7ec95c6605ce8731df4c4f8`
**(No description)**
```python
<!-- ERROR reading 83ef0f533b21b6e7ec95c6605ce8731df4c4f8: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/3f/9b6993e3b11579aed15e646c9277652f8b97d4`
**(No description)**
```python
<!-- ERROR reading 9b6993e3b11579aed15e646c9277652f8b97d4: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/3f/9dbd3b7a0b86fca0df364c7b0795ac6792a870`
**(No description)**
```python
<!-- ERROR reading 9dbd3b7a0b86fca0df364c7b0795ac6792a870: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/3f/b77bd4c70cb84e3ac14e94fa04bb378c1e62c5`
**(No description)**
```python
<!-- ERROR reading b77bd4c70cb84e3ac14e94fa04bb378c1e62c5: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/3f/f803c195243984738c6f3f328c78d9c4999cfc`
**(No description)**
```python
<!-- ERROR reading f803c195243984738c6f3f328c78d9c4999cfc: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/3f/f9756221729de65e36b534b617817bb029af22`
**(No description)**
```python
<!-- ERROR reading f9756221729de65e36b534b617817bb029af22: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/30/12cfed16b123f175b0935cd3bc4f662bd806bc`
**(No description)**
```python
<!-- ERROR reading 12cfed16b123f175b0935cd3bc4f662bd806bc: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/30/305b1f529374c2d8ee6cdfa97bd9dbdd0a87df`
**(No description)**
```python
<!-- ERROR reading 305b1f529374c2d8ee6cdfa97bd9dbdd0a87df: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/30/38ccda4c8de6ebaf1b8164a30ef7323ac07e65`
**(No description)**
```python
<!-- ERROR reading 38ccda4c8de6ebaf1b8164a30ef7323ac07e65: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/30/6c09d36ba9a43b5ded035361c4e69a924b4214`
**(No description)**
```python
<!-- ERROR reading 6c09d36ba9a43b5ded035361c4e69a924b4214: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/30/84ae51ecc94b5979ae9075ebb0e08fbda8bdbd`
**(No description)**
```python
<!-- ERROR reading 84ae51ecc94b5979ae9075ebb0e08fbda8bdbd: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/30/86427034f2177328784e2abd4b8ee1a02e73c5`
**(No description)**
```python
<!-- ERROR reading 86427034f2177328784e2abd4b8ee1a02e73c5: 'utf-8' codec can't decode byte 0xdc in position 6: invalid continuation byte -->
```

### `.git/objects/30/b856a09478eb5959cbb6be8f04fd5efcb2a5b4`
**(No description)**
```python
<!-- ERROR reading b856a09478eb5959cbb6be8f04fd5efcb2a5b4: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/30/ed4c5a62a99906ab662a8acfba2ab75e82af2e`
**(No description)**
```python
<!-- ERROR reading ed4c5a62a99906ab662a8acfba2ab75e82af2e: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/30/f304a061cb69206936409099913f03850c9fdf`
**(No description)**
```python
<!-- ERROR reading f304a061cb69206936409099913f03850c9fdf: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/5e/141aa1be706056bd8e1d923b1bde37eb7051e1`
**(No description)**
```python
<!-- ERROR reading 141aa1be706056bd8e1d923b1bde37eb7051e1: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/5e/29502cddfa9a9887a93399ab4193fb75dfe605`
**(No description)**
```python
<!-- ERROR reading 29502cddfa9a9887a93399ab4193fb75dfe605: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/5e/a609ccedf18eb4ab70f8fc6990448eb6407237`
**(No description)**
```python
<!-- ERROR reading a609ccedf18eb4ab70f8fc6990448eb6407237: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/5e/e55ecd0221aeb7469dcfe0ffbc1c6a42abecc7`
**(No description)**
```python
<!-- ERROR reading e55ecd0221aeb7469dcfe0ffbc1c6a42abecc7: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/5e/f8b36287ede5bc55704b267c20f61f47bdf0d7`
**(No description)**
```python
<!-- ERROR reading f8b36287ede5bc55704b267c20f61f47bdf0d7: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/5b/20803e586b5660fde18fe87056bbcd0dc61c1a`
**(No description)**
```python
<!-- ERROR reading 20803e586b5660fde18fe87056bbcd0dc61c1a: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/5b/2c4ad5250b589aa0c8f8d1cc9125b91b10edb0`
**(No description)**
```python
<!-- ERROR reading 2c4ad5250b589aa0c8f8d1cc9125b91b10edb0: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/5b/2de39e5fb9027d062404a94fda53f45764dd23`
**(No description)**
```python
<!-- ERROR reading 2de39e5fb9027d062404a94fda53f45764dd23: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/5b/a926e3b09a71121d3c10b962c26137221d5a34`
**(No description)**
```python
<!-- ERROR reading a926e3b09a71121d3c10b962c26137221d5a34: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/5b/ad85fdc1cd08553756d0fb2c7be8b5ad6af7fb`
**(No description)**
```python
<!-- ERROR reading ad85fdc1cd08553756d0fb2c7be8b5ad6af7fb: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/5b/b6351cb6088d8e8c4f2d602df2963c6ca02cc3`
**(No description)**
```python
<!-- ERROR reading b6351cb6088d8e8c4f2d602df2963c6ca02cc3: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/5b/f0c9723f171f91a5952b57c4aafb8cee3c6acd`
**(No description)**
```python
<!-- ERROR reading f0c9723f171f91a5952b57c4aafb8cee3c6acd: 'utf-8' codec can't decode byte 0xc8 in position 17: invalid continuation byte -->
```

### `.git/objects/37/783d4d12cb8809a8df0e5950b7271ba46f1c0e`
**(No description)**
```python
<!-- ERROR reading 783d4d12cb8809a8df0e5950b7271ba46f1c0e: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/37/af27a728c0a60ab18c7c435352c3fca1880d44`
**(No description)**
```python
<!-- ERROR reading af27a728c0a60ab18c7c435352c3fca1880d44: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/37/db4d6cd7539940d5629ae1f426526a4d8d1d6f`
**(No description)**
```python
<!-- ERROR reading db4d6cd7539940d5629ae1f426526a4d8d1d6f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/08/0f22a3b5923f9d32b955a0c432b35a7e11c2b2`
**(No description)**
```python
<!-- ERROR reading 0f22a3b5923f9d32b955a0c432b35a7e11c2b2: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/08/2f8b2a26b673d640699a6c6da0586190b446cc`
**(No description)**
```python
<!-- ERROR reading 2f8b2a26b673d640699a6c6da0586190b446cc: 'utf-8' codec can't decode byte 0xd1 in position 21: invalid continuation byte -->
```

### `.git/objects/08/63a1883e72058a8701a946c644276f047f837e`
**(No description)**
```python
<!-- ERROR reading 63a1883e72058a8701a946c644276f047f837e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/08/6ad46e1d677e2809001cabaa3e9235f664ec68`
**(No description)**
```python
<!-- ERROR reading 6ad46e1d677e2809001cabaa3e9235f664ec68: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/08/6b64dd3817c0c1a194ffc1959eeffdd2695bef`
**(No description)**
```python
<!-- ERROR reading 6b64dd3817c0c1a194ffc1959eeffdd2695bef: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/08/8831eb5c347e22db419f30380f3c0dd740a08c`
**(No description)**
```python
<!-- ERROR reading 8831eb5c347e22db419f30380f3c0dd740a08c: 'utf-8' codec can't decode byte 0x85 in position 14: invalid start byte -->
```

### `.git/objects/08/88a8263b20afb58a9f11d8b81f79d89e624935`
**(No description)**
```python
<!-- ERROR reading 88a8263b20afb58a9f11d8b81f79d89e624935: 'utf-8' codec can't decode byte 0x85 in position 14: invalid start byte -->
```

### `.git/objects/08/8e977b5b1614dda8c8429393f6acd325b11e08`
**(No description)**
```python
<!-- ERROR reading 8e977b5b1614dda8c8429393f6acd325b11e08: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/08/a9574da4a89d82dfb71b3087b14c8644102dd6`
**(No description)**
```python
<!-- ERROR reading a9574da4a89d82dfb71b3087b14c8644102dd6: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/08/b7ddbd54f906d56d66a95408f1c9b6313c4a1c`
**(No description)**
```python
<!-- ERROR reading b7ddbd54f906d56d66a95408f1c9b6313c4a1c: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/08/c826ff6d43a7e34be0adfd28f7f542ec3c21f2`
**(No description)**
```python
<!-- ERROR reading c826ff6d43a7e34be0adfd28f7f542ec3c21f2: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/08/d7e035315677856fd2cd0be2044689b57619bf`
**(No description)**
```python
<!-- ERROR reading d7e035315677856fd2cd0be2044689b57619bf: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/08/fd13678a1c4dffe3e126acf0167c17d62c2ed8`
**(No description)**
```python
<!-- ERROR reading fd13678a1c4dffe3e126acf0167c17d62c2ed8: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/6d/1fe20b406b3e7beeb564927cf3a3f48de4381e`
**(No description)**
```python
<!-- ERROR reading 1fe20b406b3e7beeb564927cf3a3f48de4381e: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/6d/427cdc2786797715766efb20ff87a1030e1a57`
**(No description)**
```python
<!-- ERROR reading 427cdc2786797715766efb20ff87a1030e1a57: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6d/58a6f30238a3c8dc9de54e3bd41772d7a2a848`
**(No description)**
```python
<!-- ERROR reading 58a6f30238a3c8dc9de54e3bd41772d7a2a848: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/6d/62a67e48586a3bd92a3ac94b92aaa5e72f036d`
**(No description)**
```python
<!-- ERROR reading 62a67e48586a3bd92a3ac94b92aaa5e72f036d: 'utf-8' codec can't decode byte 0xcf in position 23: invalid continuation byte -->
```

### `.git/objects/6d/6f93aabd44902caf086998226aa48fd3bbe221`
**(No description)**
```python
<!-- ERROR reading 6f93aabd44902caf086998226aa48fd3bbe221: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/6d/cb45898184ec7ea5143e42bd147138fd8ed304`
**(No description)**
```python
<!-- ERROR reading cb45898184ec7ea5143e42bd147138fd8ed304: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/6d/e4198fcc39b317cc664bf389f2fc5646e167eb`
**(No description)**
```python
<!-- ERROR reading e4198fcc39b317cc664bf389f2fc5646e167eb: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/6d/f00c9114f71ec98bc82863076812299c98b80c`
**(No description)**
```python
<!-- ERROR reading f00c9114f71ec98bc82863076812299c98b80c: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/6d/f5a707cc31fc0b6eda65a5fc61d972819f315a`
**(No description)**
```python
<!-- ERROR reading f5a707cc31fc0b6eda65a5fc61d972819f315a: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/01/0c3620d4a28eb8ec762025c280d877904ea3e6`
**(No description)**
```python
<!-- ERROR reading 0c3620d4a28eb8ec762025c280d877904ea3e6: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/01/4871d280edb57971aa1eb0fbe26862ce43bf53`
**(No description)**
```python
<!-- ERROR reading 4871d280edb57971aa1eb0fbe26862ce43bf53: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/01/74bcce6d48de946214d59bcae5543d38d89c3a`
**(No description)**
```python
<!-- ERROR reading 74bcce6d48de946214d59bcae5543d38d89c3a: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/01/c650244d0ccb6043c603b736fcf8d9e622bc71`
**(No description)**
```python
<!-- ERROR reading c650244d0ccb6043c603b736fcf8d9e622bc71: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/01/c6cf679f9aaecce66bc988432ff3fa56a580b5`
**(No description)**
```python
<!-- ERROR reading c6cf679f9aaecce66bc988432ff3fa56a580b5: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/01/d1743111c495783f149af5cc328908c39d09cc`
**(No description)**
```python
<!-- ERROR reading d1743111c495783f149af5cc328908c39d09cc: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/06/11b62a3a80fc60b7c7cc4bae917245e0a82b7e`
**(No description)**
```python
<!-- ERROR reading 11b62a3a80fc60b7c7cc4bae917245e0a82b7e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/06/2c98f2489951a9b215c5f02d7cdb71605ec1b3`
**(No description)**
```python
<!-- ERROR reading 2c98f2489951a9b215c5f02d7cdb71605ec1b3: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/06/3d6ea4a3a1d0cbab8bed3ade9aa7f3bfc507ca`
**(No description)**
```python
<!-- ERROR reading 3d6ea4a3a1d0cbab8bed3ade9aa7f3bfc507ca: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/06/8ea457a16cb693f08c6ad48bd4fe2d96e70c86`
**(No description)**
```python
<!-- ERROR reading 8ea457a16cb693f08c6ad48bd4fe2d96e70c86: 'utf-8' codec can't decode byte 0x8c in position 2: invalid start byte -->
```

### `.git/objects/06/a594e58f6746041edf371bc3dc8ca42b612322`
**(No description)**
```python
<!-- ERROR reading a594e58f6746041edf371bc3dc8ca42b612322: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/06/fdf295eeb6ae0a513f145077bf57c3bde3a9a3`
**(No description)**
```python
<!-- ERROR reading fdf295eeb6ae0a513f145077bf57c3bde3a9a3: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/6c/0731310faee176edce2314ca4bb9010ec92fff`
**(No description)**
```python
<!-- ERROR reading 0731310faee176edce2314ca4bb9010ec92fff: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6c/0e9790d5d0764f2ca005ae955d644bc2098d75`
**(No description)**
```python
<!-- ERROR reading 0e9790d5d0764f2ca005ae955d644bc2098d75: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/6c/2ba7fedf9337260824b62987e65301e4fed129`
**(No description)**
```python
<!-- ERROR reading 2ba7fedf9337260824b62987e65301e4fed129: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/6c/3196cc2d7e46e6756580267f5643c6f7b448dd`
**(No description)**
```python
<!-- ERROR reading 3196cc2d7e46e6756580267f5643c6f7b448dd: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/6c/78573d6dc2fe0cd9eee007f45c9f60e0451e93`
**(No description)**
```python
<!-- ERROR reading 78573d6dc2fe0cd9eee007f45c9f60e0451e93: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/6c/88b8901b2a78b1a2a7be11372eea04aed93d1e`
**(No description)**
```python
<!-- ERROR reading 88b8901b2a78b1a2a7be11372eea04aed93d1e: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/6c/8db6f3353fffa953aa8efdd89739e2bda4c476`
**(No description)**
```python
<!-- ERROR reading 8db6f3353fffa953aa8efdd89739e2bda4c476: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/6c/f6c60bda53422d58fd2d278dbfee95657f3a8d`
**(No description)**
```python
<!-- ERROR reading f6c60bda53422d58fd2d278dbfee95657f3a8d: 'utf-8' codec can't decode byte 0xb4 in position 2: invalid start byte -->
```

### `.git/objects/39/060604e7524f1b88df372c5d20aa6d5a57f2a7`
**(No description)**
```python
<!-- ERROR reading 060604e7524f1b88df372c5d20aa6d5a57f2a7: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/39/134557d6e60685fe34e2bc06769282ee68b600`
**(No description)**
```python
<!-- ERROR reading 134557d6e60685fe34e2bc06769282ee68b600: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/39/6c09de21e7d68d9d0739fcfd3f7a409bb218fc`
**(No description)**
```python
<!-- ERROR reading 6c09de21e7d68d9d0739fcfd3f7a409bb218fc: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/39/8386a5b9f61c13be314e256e671a37d28e3623`
**(No description)**
```python
<!-- ERROR reading 8386a5b9f61c13be314e256e671a37d28e3623: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/39/a18fd6cb0e3cbd89886de183ef7ce294faef95`
**(No description)**
```python
<!-- ERROR reading a18fd6cb0e3cbd89886de183ef7ce294faef95: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/39/a24b04888e79df51e2237577b303a2f901be63`
**(No description)**
```python
<!-- ERROR reading a24b04888e79df51e2237577b303a2f901be63: 'utf-8' codec can't decode byte 0xcc in position 3: invalid continuation byte -->
```

### `.git/objects/39/a2b01cd2f5a925e081683d113baf634263d75b`
**(No description)**
```python
<!-- ERROR reading a2b01cd2f5a925e081683d113baf634263d75b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/39/d978686d1e836b3fd676c9e29c7f7a58e82432`
**(No description)**
```python
<!-- ERROR reading d978686d1e836b3fd676c9e29c7f7a58e82432: 'utf-8' codec can't decode byte 0xa9 in position 19: invalid start byte -->
```

### `.git/objects/99/16c3ab031b139d6a09373fe053a3cecdd56852`
**(No description)**
```python
<!-- ERROR reading 16c3ab031b139d6a09373fe053a3cecdd56852: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/99/77150c92fcb083fcdfa632c9de3b5fa92470cb`
**(No description)**
```python
<!-- ERROR reading 77150c92fcb083fcdfa632c9de3b5fa92470cb: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/99/98dd815b53f1f643cf4eee38af342013e5ab8b`
**(No description)**
```python
<!-- ERROR reading 98dd815b53f1f643cf4eee38af342013e5ab8b: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/99/b0f5e6a33b6ec1d83ecc87834408cd7dc14835`
**(No description)**
```python
<!-- ERROR reading b0f5e6a33b6ec1d83ecc87834408cd7dc14835: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/99/b8adfad5553e5b69648ea28de613f0f661ab82`
**(No description)**
```python
<!-- ERROR reading b8adfad5553e5b69648ea28de613f0f661ab82: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/99/dee974a6402f82d6718adb486dc94dd74f4b13`
**(No description)**
```python
<!-- ERROR reading dee974a6402f82d6718adb486dc94dd74f4b13: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/99/ebea30c91443c89e7d61909b6cba6836794a43`
**(No description)**
```python
<!-- ERROR reading ebea30c91443c89e7d61909b6cba6836794a43: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/52/024887a7f94570055873041d2a25ed6497bd60`
**(No description)**
```python
<!-- ERROR reading 024887a7f94570055873041d2a25ed6497bd60: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/52/1abd7c2ca633f90a5ba13a8060c5c3d0c32205`
**(No description)**
```python
<!-- ERROR reading 1abd7c2ca633f90a5ba13a8060c5c3d0c32205: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/52/1eb716a5ebbcbc2c59654c4e71c3f0ff1abf26`
**(No description)**
```python
<!-- ERROR reading 1eb716a5ebbcbc2c59654c4e71c3f0ff1abf26: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/52/62c8323eae2d5bf41164a30f6a539a467ddb00`
**(No description)**
```python
<!-- ERROR reading 62c8323eae2d5bf41164a30f6a539a467ddb00: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/52/d5bead2487c821915794433a913703978819d0`
**(No description)**
```python
<!-- ERROR reading d5bead2487c821915794433a913703978819d0: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/52/da22e82574362866535edac8388616cd5c91a4`
**(No description)**
```python
<!-- ERROR reading da22e82574362866535edac8388616cd5c91a4: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/52/dae2594c525da9a4c0415589e72d106be02f2c`
**(No description)**
```python
<!-- ERROR reading dae2594c525da9a4c0415589e72d106be02f2c: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/55/0cbfa1e28a2376fe1b4f994bce86b446c0916e`
**(No description)**
```python
<!-- ERROR reading 0cbfa1e28a2376fe1b4f994bce86b446c0916e: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/55/94452b55bed63346b36a9647e663e874095412`
**(No description)**
```python
<!-- ERROR reading 94452b55bed63346b36a9647e663e874095412: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/55/a4ac4a1a918720bb3b94eaea6f8737b968216a`
**(No description)**
```python
<!-- ERROR reading a4ac4a1a918720bb3b94eaea6f8737b968216a: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/97/0033ecca401c984a3de3c6e4824d7aefa34b87`
**(No description)**
```python
<!-- ERROR reading 0033ecca401c984a3de3c6e4824d7aefa34b87: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/97/6a3ba242e3e9f94e4f6fd07de8a29f837e580d`
**(No description)**
```python
<!-- ERROR reading 6a3ba242e3e9f94e4f6fd07de8a29f837e580d: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/97/7e5d2934016630108499c24c1f6fd5bf30179a`
**(No description)**
```python
<!-- ERROR reading 7e5d2934016630108499c24c1f6fd5bf30179a: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/97/fc82103181396d739f5d940b1b9f79d881f9ed`
**(No description)**
```python
<!-- ERROR reading fc82103181396d739f5d940b1b9f79d881f9ed: 'utf-8' codec can't decode byte 0xcd in position 4: invalid continuation byte -->
```

### `.git/objects/63/2854d3bc59aa10c0bb6ec49ccc9712babfda6c`
**(No description)**
```python
<!-- ERROR reading 2854d3bc59aa10c0bb6ec49ccc9712babfda6c: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/63/56c770c7d1f26ef4f90a4781b1386209f8169c`
**(No description)**
```python
<!-- ERROR reading 56c770c7d1f26ef4f90a4781b1386209f8169c: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/63/58c0451b2d0036e3821d897fb6f7ab436ee4a9`
**(No description)**
```python
<!-- ERROR reading 58c0451b2d0036e3821d897fb6f7ab436ee4a9: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/63/7da64802d0360b901ef369c0a121b1b75ef773`
**(No description)**
```python
<!-- ERROR reading 7da64802d0360b901ef369c0a121b1b75ef773: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/63/8102f771dd674799255cc6ef69cacb2c184d13`
**(No description)**
```python
<!-- ERROR reading 8102f771dd674799255cc6ef69cacb2c184d13: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/63/b58d71aca3126558e8d73bff86b3b3de4b6617`
**(No description)**
```python
<!-- ERROR reading b58d71aca3126558e8d73bff86b3b3de4b6617: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/63/c828524f97c78e8059fcf6e3598ca01f4df46c`
**(No description)**
```python
<!-- ERROR reading c828524f97c78e8059fcf6e3598ca01f4df46c: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/63/dee4d53c3453cfc195e3149f81f2158f6c6ecb`
**(No description)**
```python
<!-- ERROR reading dee4d53c3453cfc195e3149f81f2158f6c6ecb: 'utf-8' codec can't decode byte 0xcd in position 22: invalid continuation byte -->
```

### `.git/objects/63/ea99016e031b2288460201522c111a4f5f9551`
**(No description)**
```python
<!-- ERROR reading ea99016e031b2288460201522c111a4f5f9551: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/63/f2f19e409c7f4b3c6c064022e8f104227873aa`
**(No description)**
```python
<!-- ERROR reading f2f19e409c7f4b3c6c064022e8f104227873aa: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/0f/32b5f6207441753482e8b24e0f4ff10c5614d8`
**(No description)**
```python
<!-- ERROR reading 32b5f6207441753482e8b24e0f4ff10c5614d8: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/0f/3317a001c4bcfbf9a9296ea9d898ef6430c4c6`
**(No description)**
```python
<!-- ERROR reading 3317a001c4bcfbf9a9296ea9d898ef6430c4c6: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/0f/70284822f50098e21ad439550cdbd4d298d011`
**(No description)**
```python
<!-- ERROR reading 70284822f50098e21ad439550cdbd4d298d011: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/0f/7d282aa5df08f3e2692bf1e51dfaaea60ae4ea`
**(No description)**
```python
<!-- ERROR reading 7d282aa5df08f3e2692bf1e51dfaaea60ae4ea: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/0f/ac94e9e54905688d0e359fc5a9b96b703afab5`
**(No description)**
```python
<!-- ERROR reading ac94e9e54905688d0e359fc5a9b96b703afab5: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/0f/db4ec4e91090876dc3fbf207049b521fa0dd73`
**(No description)**
```python
<!-- ERROR reading db4ec4e91090876dc3fbf207049b521fa0dd73: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0a/13c9d7aca12a0f10b1fcd206fcfaab1a16cb61`
**(No description)**
```python
<!-- ERROR reading 13c9d7aca12a0f10b1fcd206fcfaab1a16cb61: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/0a/90c300ba83967a50ca0fe7dfbcd5c1406914eb`
**(No description)**
```python
<!-- ERROR reading 90c300ba83967a50ca0fe7dfbcd5c1406914eb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0a/b3dd9474dedd946540a4cc01ceed577afddf5e`
**(No description)**
```python
<!-- ERROR reading b3dd9474dedd946540a4cc01ceed577afddf5e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/0a/df63df9e144a7f94ab3149894c7455a21b3b32`
**(No description)**
```python
<!-- ERROR reading df63df9e144a7f94ab3149894c7455a21b3b32: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/64/aeb506367c07515ed1ab61c874580da362ced4`
**(No description)**
```python
<!-- ERROR reading aeb506367c07515ed1ab61c874580da362ced4: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/64/b991e898ba046168e0036b1939a69510aa2d77`
**(No description)**
```python
<!-- ERROR reading b991e898ba046168e0036b1939a69510aa2d77: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/64/f06dd4bce4d634946bb836d56eff78196e0b6d`
**(No description)**
```python
<!-- ERROR reading f06dd4bce4d634946bb836d56eff78196e0b6d: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/90/108eca9047baa1b7122ff00d77be942940a6a6`
**(No description)**
```python
<!-- ERROR reading 108eca9047baa1b7122ff00d77be942940a6a6: 'utf-8' codec can't decode byte 0xbd in position 4: invalid start byte -->
```

### `.git/objects/90/341e74749349ce1f68f38391c56005e6c13533`
**(No description)**
```python
<!-- ERROR reading 341e74749349ce1f68f38391c56005e6c13533: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/90/3bd7a0567b50f15aa518bf5ad310b13608ac2c`
**(No description)**
```python
<!-- ERROR reading 3bd7a0567b50f15aa518bf5ad310b13608ac2c: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/90/60c1026e4b9319de4937d5132483bca4d309eb`
**(No description)**
```python
<!-- ERROR reading 60c1026e4b9319de4937d5132483bca4d309eb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/90/64910b8bafe2d60ce5fca8897226f5e0fb8f8f`
**(No description)**
```python
<!-- ERROR reading 64910b8bafe2d60ce5fca8897226f5e0fb8f8f: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/90/9ead571be07431ea978bf432aada2e4e8d259b`
**(No description)**
```python
<!-- ERROR reading 9ead571be07431ea978bf432aada2e4e8d259b: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/90/a6465f9682c886363eea5327dac64bf623a6ff`
**(No description)**
```python
<!-- ERROR reading a6465f9682c886363eea5327dac64bf623a6ff: 'utf-8' codec can't decode byte 0x84 in position 6: invalid start byte -->
```

### `.git/objects/90/abcdab036d3a3a5153922401d0cbb9ffe458e3`
**(No description)**
```python
<!-- ERROR reading abcdab036d3a3a5153922401d0cbb9ffe458e3: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/bf/190fd560ee4fc8a11af371a15fc5f1dc284d34`
**(No description)**
```python
<!-- ERROR reading 190fd560ee4fc8a11af371a15fc5f1dc284d34: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/bf/3cae53e3dc2083daa85288984b42137fe26848`
**(No description)**
```python
<!-- ERROR reading 3cae53e3dc2083daa85288984b42137fe26848: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/bf/4ea5038778289624815e650bc779c04386680b`
**(No description)**
```python
<!-- ERROR reading 4ea5038778289624815e650bc779c04386680b: 'utf-8' codec can't decode byte 0xb1 in position 8: invalid start byte -->
```

### `.git/objects/bf/85c7e3a488fc669e3840400a4f1f3b58fcbbb1`
**(No description)**
```python
<!-- ERROR reading 85c7e3a488fc669e3840400a4f1f3b58fcbbb1: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/bf/9b642fab36adcd5987c3687d42f36a9b6b49c1`
**(No description)**
```python
<!-- ERROR reading 9b642fab36adcd5987c3687d42f36a9b6b49c1: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/bf/c40e2ae0efddee75d0328cbe83720b8d80d886`
**(No description)**
```python
<!-- ERROR reading c40e2ae0efddee75d0328cbe83720b8d80d886: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/bf/fb3cd653e541819fcefe06d5e4a09383809286`
**(No description)**
```python
<!-- ERROR reading fb3cd653e541819fcefe06d5e4a09383809286: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d3/2929906dc6d434a2b43a2b58bc6b14accf314c`
**(No description)**
```python
<!-- ERROR reading 2929906dc6d434a2b43a2b58bc6b14accf314c: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/d3/927370f703c15b98364d11c207809b37f6efe5`
**(No description)**
```python
<!-- ERROR reading 927370f703c15b98364d11c207809b37f6efe5: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/d3/b90a8e63afc72a03c0f277bb464222fef4927c`
**(No description)**
```python
<!-- ERROR reading b90a8e63afc72a03c0f277bb464222fef4927c: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/d4/4447eaf5a3912ea699e6d895d51f9b0782cfba`
**(No description)**
```python
<!-- ERROR reading 4447eaf5a3912ea699e6d895d51f9b0782cfba: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/d4/48a2117bc78bef026692317603e26e63bd0c34`
**(No description)**
```python
<!-- ERROR reading 48a2117bc78bef026692317603e26e63bd0c34: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d4/5cfb36815d3d94ae232c1b2aaed94f284d2437`
**(No description)**
```python
<!-- ERROR reading 5cfb36815d3d94ae232c1b2aaed94f284d2437: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/d4/cc378bb6148de2222308e07b3eb898f1f297d2`
**(No description)**
```python
<!-- ERROR reading cc378bb6148de2222308e07b3eb898f1f297d2: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/ba/07b74867b83beaaabc3afe2e19d77d71544338`
**(No description)**
```python
<!-- ERROR reading 07b74867b83beaaabc3afe2e19d77d71544338: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/ba/50acb0624e1da7d613d8a700e313b46e76624e`
**(No description)**
```python
<!-- ERROR reading 50acb0624e1da7d613d8a700e313b46e76624e: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/ba/53d088f6f8d22dede47873a03b70a7103da7ea`
**(No description)**
```python
<!-- ERROR reading 53d088f6f8d22dede47873a03b70a7103da7ea: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ba/b11b80c60f10a4f3bccb12eb5b17c48a449767`
**(No description)**
```python
<!-- ERROR reading b11b80c60f10a4f3bccb12eb5b17c48a449767: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/ba/b98d675883cc7567a79df485cd7b4f015e376f`
**(No description)**
```python
<!-- ERROR reading b98d675883cc7567a79df485cd7b4f015e376f: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/ba/ca1afabe94f3cf7a9309d8f11258a94fb19f06`
**(No description)**
```python
<!-- ERROR reading ca1afabe94f3cf7a9309d8f11258a94fb19f06: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/a0/19bc77bdda90d3af6f4cbe1294ede2ff5dd18f`
**(No description)**
```python
<!-- ERROR reading 19bc77bdda90d3af6f4cbe1294ede2ff5dd18f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/a0/86215f978ca6095f3b4210d097a6035d01f04e`
**(No description)**
```python
<!-- ERROR reading 86215f978ca6095f3b4210d097a6035d01f04e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a0/cf67df5245be16a020ca048832e180f7ce8661`
**(No description)**
```python
<!-- ERROR reading cf67df5245be16a020ca048832e180f7ce8661: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/a0/d619842fb7eab0cfa8427ce615bbafd4acd193`
**(No description)**
```python
<!-- ERROR reading d619842fb7eab0cfa8427ce615bbafd4acd193: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/a0/fbf62af8a7bfb7d857d8f07644ce479050e9b0`
**(No description)**
```python
<!-- ERROR reading fbf62af8a7bfb7d857d8f07644ce479050e9b0: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/a7/0fd58ce202974a1aef37fc1db73c2ee39c7491`
**(No description)**
```python
<!-- ERROR reading 0fd58ce202974a1aef37fc1db73c2ee39c7491: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a7/2c2c5f70eafdf0229332ccf3c1284b2955ea56`
**(No description)**
```python
<!-- ERROR reading 2c2c5f70eafdf0229332ccf3c1284b2955ea56: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/a7/598fc6c56688c4dd6526fc6e8b8e03682f62e8`
**(No description)**
```python
<!-- ERROR reading 598fc6c56688c4dd6526fc6e8b8e03682f62e8: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/a7/9a86106edd7d255d1fde0c73feafe853d7a164`
**(No description)**
```python
<!-- ERROR reading 9a86106edd7d255d1fde0c73feafe853d7a164: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/a7/a5711dbf1f401692cca41f67f8cb78fc70af8a`
**(No description)**
```python
<!-- ERROR reading a5711dbf1f401692cca41f67f8cb78fc70af8a: 'utf-8' codec can't decode byte 0xdc in position 6: invalid continuation byte -->
```

### `.git/objects/a7/bd483429520dee0c989e516477c51ca12f4638`
**(No description)**
```python
<!-- ERROR reading bd483429520dee0c989e516477c51ca12f4638: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a7/bf20d891beeb2b01c48ee9814341171c577696`
**(No description)**
```python
<!-- ERROR reading bf20d891beeb2b01c48ee9814341171c577696: 'utf-8' codec can't decode byte 0xcc in position 19: invalid continuation byte -->
```

### `.git/objects/a7/fc697a872a68ce7fad3f62cdc39e3b162c06d7`
**(No description)**
```python
<!-- ERROR reading fc697a872a68ce7fad3f62cdc39e3b162c06d7: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b8/0cc04f64cf033812e5fcba992db0e274f821be`
**(No description)**
```python
<!-- ERROR reading 0cc04f64cf033812e5fcba992db0e274f821be: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b8/10cd2ce908a14d08556cf2913e3772ad2d312e`
**(No description)**
```python
<!-- ERROR reading 10cd2ce908a14d08556cf2913e3772ad2d312e: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b8/140cf1ae7cd6d84a484668608ec6226db20e37`
**(No description)**
```python
<!-- ERROR reading 140cf1ae7cd6d84a484668608ec6226db20e37: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/b8/140db7a2359df9cb827e309ea2bd6332afad53`
**(No description)**
```python
<!-- ERROR reading 140db7a2359df9cb827e309ea2bd6332afad53: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/b8/1849e1ef82b793f6f81bb970cdc3cb791f5776`
**(No description)**
```python
<!-- ERROR reading 1849e1ef82b793f6f81bb970cdc3cb791f5776: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b8/266b9a60f8c363ba35f7b73befd7c9c7cb4abc`
**(No description)**
```python
<!-- ERROR reading 266b9a60f8c363ba35f7b73befd7c9c7cb4abc: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/b8/2c89c5571c7707f3d426c928ea247e8c2d7172`
**(No description)**
```python
<!-- ERROR reading 2c89c5571c7707f3d426c928ea247e8c2d7172: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/b8/6a3e06e429aa1bdd67713a3d4998410375dd49`
**(No description)**
```python
<!-- ERROR reading 6a3e06e429aa1bdd67713a3d4998410375dd49: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/b8/a0adbbb97ea11f36eb0c6b2a3c2881e96f8e26`
**(No description)**
```python
<!-- ERROR reading a0adbbb97ea11f36eb0c6b2a3c2881e96f8e26: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b8/afe2c1bbf75df3718ce621c7bac358d2612483`
**(No description)**
```python
<!-- ERROR reading afe2c1bbf75df3718ce621c7bac358d2612483: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b8/bb97185926d7daed314609753173945ed4ff1a`
**(No description)**
```python
<!-- ERROR reading bb97185926d7daed314609753173945ed4ff1a: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/b8/cdde3abf6045ad99f3c43d312719b078a75369`
**(No description)**
```python
<!-- ERROR reading cdde3abf6045ad99f3c43d312719b078a75369: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/b8/da1ccc7db5dfe0d0b9add1ee98de5de1a201fd`
**(No description)**
```python
<!-- ERROR reading da1ccc7db5dfe0d0b9add1ee98de5de1a201fd: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b8/fb2154b6d0618b62281578e5e947bca487cee4`
**(No description)**
```python
<!-- ERROR reading fb2154b6d0618b62281578e5e947bca487cee4: 'utf-8' codec can't decode byte 0xef in position 4: invalid continuation byte -->
```

### `.git/objects/b1/487b7819e7286577a043c7726fbe0ca1543083`
**(No description)**
```python
<!-- ERROR reading 487b7819e7286577a043c7726fbe0ca1543083: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/b1/49ed79b0a1d5808a7e392876c2f5aae4b5057c`
**(No description)**
```python
<!-- ERROR reading 49ed79b0a1d5808a7e392876c2f5aae4b5057c: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/b1/c5158c0fe2b4d11a90a9c632fb8f640cdb6f9d`
**(No description)**
```python
<!-- ERROR reading c5158c0fe2b4d11a90a9c632fb8f640cdb6f9d: 'utf-8' codec can't decode byte 0xb7 in position 8: invalid start byte -->
```

### `.git/objects/b1/e77fa06fe0d7b2ecbda61147b48803991afe37`
**(No description)**
```python
<!-- ERROR reading e77fa06fe0d7b2ecbda61147b48803991afe37: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/b1/fbbf8e8d2a47d0a7d2fe0b4568fd11f8be4c36`
**(No description)**
```python
<!-- ERROR reading fbbf8e8d2a47d0a7d2fe0b4568fd11f8be4c36: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/dd/6dcbe651c458343d26a2f6b55481b2184e993a`
**(No description)**
```python
<!-- ERROR reading 6dcbe651c458343d26a2f6b55481b2184e993a: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/dd/bd551da04e6763e384f84c7a62fb454ebd5a6c`
**(No description)**
```python
<!-- ERROR reading bd551da04e6763e384f84c7a62fb454ebd5a6c: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/dd/becaa26f9565b53d0d2f364bf6d4e1ca8682c0`
**(No description)**
```python
<!-- ERROR reading becaa26f9565b53d0d2f364bf6d4e1ca8682c0: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/dd/cc189001c50c37c6a03810dc21d955df919f10`
**(No description)**
```python
<!-- ERROR reading cc189001c50c37c6a03810dc21d955df919f10: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/dd/d2a2f825f206164eb9efb0a5c41528365beb85`
**(No description)**
```python
<!-- ERROR reading d2a2f825f206164eb9efb0a5c41528365beb85: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/dd/e5de8a2ce444aa3dc30963e36094e6b73d7267`
**(No description)**
```python
<!-- ERROR reading e5de8a2ce444aa3dc30963e36094e6b73d7267: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/dc/11514da71f1fc18262fcd480a4b162a75249a7`
**(No description)**
```python
<!-- ERROR reading 11514da71f1fc18262fcd480a4b162a75249a7: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/dc/550efc74a77aff4a12e543e2d03043d0e1e447`
**(No description)**
```python
<!-- ERROR reading 550efc74a77aff4a12e543e2d03043d0e1e447: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/dc/5d1f01b4d8ae42eea7350c258e98c9515d006b`
**(No description)**
```python
<!-- ERROR reading 5d1f01b4d8ae42eea7350c258e98c9515d006b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/dc/5f1a04d2ebaaac138fff93be5dc1f153145078`
**(No description)**
```python
<!-- ERROR reading 5f1a04d2ebaaac138fff93be5dc1f153145078: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/dc/896c766c1edf89b0126010ff9fa77eb14a3e73`
**(No description)**
```python
<!-- ERROR reading 896c766c1edf89b0126010ff9fa77eb14a3e73: 'utf-8' codec can't decode byte 0xcf in position 3: invalid continuation byte -->
```

### `.git/objects/dc/e5c32f7e4ae1a03d8a4a948ae186c8f63abcc2`
**(No description)**
```python
<!-- ERROR reading e5c32f7e4ae1a03d8a4a948ae186c8f63abcc2: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/b6/0840b5a254b6cb37721283ef82365d4097844b`
**(No description)**
```python
<!-- ERROR reading 0840b5a254b6cb37721283ef82365d4097844b: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/b6/2234d50750cbcf6d3ebba02d2ee54afb8c7347`
**(No description)**
```python
<!-- ERROR reading 2234d50750cbcf6d3ebba02d2ee54afb8c7347: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/b6/24e7de664ae6f61eef5843d120708851f6f8e3`
**(No description)**
```python
<!-- ERROR reading 24e7de664ae6f61eef5843d120708851f6f8e3: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/b6/7f02ccaf821ac212e89fe322f829bc2d518665`
**(No description)**
```python
<!-- ERROR reading 7f02ccaf821ac212e89fe322f829bc2d518665: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/b6/8078cb9680de4cca65b1145632a37c5e751c38`
**(No description)**
```python
<!-- ERROR reading 8078cb9680de4cca65b1145632a37c5e751c38: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/b6/863d934050634930dae8a634ada52e547c29bf`
**(No description)**
```python
<!-- ERROR reading 863d934050634930dae8a634ada52e547c29bf: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/b6/9088f2588d2296adbacd80ba77e103e2265db2`
**(No description)**
```python
<!-- ERROR reading 9088f2588d2296adbacd80ba77e103e2265db2: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b6/94c6bad3ddad4208923dd917713129a8490874`
**(No description)**
```python
<!-- ERROR reading 94c6bad3ddad4208923dd917713129a8490874: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/b6/aaa0d13ed4441bb5a4adeebdd0a404c2efc285`
**(No description)**
```python
<!-- ERROR reading aaa0d13ed4441bb5a4adeebdd0a404c2efc285: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b6/beddbe6d24d2949dc89ed07abfebd59d8b63b9`
**(No description)**
```python
<!-- ERROR reading beddbe6d24d2949dc89ed07abfebd59d8b63b9: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/a9/1fe2cd4ae12e619a0ca34baf14400ded5f14cf`
**(No description)**
```python
<!-- ERROR reading 1fe2cd4ae12e619a0ca34baf14400ded5f14cf: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a9/adb8b6c85412eff2a43197f748b6d5dd9a8b6e`
**(No description)**
```python
<!-- ERROR reading adb8b6c85412eff2a43197f748b6d5dd9a8b6e: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/d5/25de5c6c8791def8dbb2f460027e200c934874`
**(No description)**
```python
<!-- ERROR reading 25de5c6c8791def8dbb2f460027e200c934874: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/d5/4025e52d7ec2996d3a6fbdea9c390291067063`
**(No description)**
```python
<!-- ERROR reading 4025e52d7ec2996d3a6fbdea9c390291067063: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d5/43798f75a08b1c678964eeefef9addcb9f9e0d`
**(No description)**
```python
<!-- ERROR reading 43798f75a08b1c678964eeefef9addcb9f9e0d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d5/636645bd37d0ee826cb22a00981131ba57be17`
**(No description)**
```python
<!-- ERROR reading 636645bd37d0ee826cb22a00981131ba57be17: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/d5/64d0bc3dd917926892c55e3706cc116d5b165e`
**(No description)**
```python
<!-- ERROR reading 64d0bc3dd917926892c55e3706cc116d5b165e: 'utf-8' codec can't decode byte 0xd0 in position 17: invalid continuation byte -->
```

### `.git/objects/d5/669d8c149923d2eb8ac5c5289ecb7d4ed3e532`
**(No description)**
```python
<!-- ERROR reading 669d8c149923d2eb8ac5c5289ecb7d4ed3e532: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/d5/712f33502ff3596c72217ac7e421e8cda78ff5`
**(No description)**
```python
<!-- ERROR reading 712f33502ff3596c72217ac7e421e8cda78ff5: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/d5/a91601a8f76cdec2d0348421af6871de1e8d2e`
**(No description)**
```python
<!-- ERROR reading a91601a8f76cdec2d0348421af6871de1e8d2e: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/d5/aa05ff234fd3fbf4fee88c4a7d3e3c151a538f`
**(No description)**
```python
<!-- ERROR reading aa05ff234fd3fbf4fee88c4a7d3e3c151a538f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d5/c4c9de591a80779ddda1e3e82d4745d7dbab4f`
**(No description)**
```python
<!-- ERROR reading c4c9de591a80779ddda1e3e82d4745d7dbab4f: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/d5/cd8e3e24f46a8d4610717d76fb3ef9ad80b643`
**(No description)**
```python
<!-- ERROR reading cd8e3e24f46a8d4610717d76fb3ef9ad80b643: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/d2/1d697c887bed1f8ab7f36d10185e986d9f1e54`
**(No description)**
```python
<!-- ERROR reading 1d697c887bed1f8ab7f36d10185e986d9f1e54: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d2/445c93f5d753165a8711b54ac36fc816d8b03a`
**(No description)**
```python
<!-- ERROR reading 445c93f5d753165a8711b54ac36fc816d8b03a: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/d2/5ce2fcbee3817b0fb095bc7648371948aad429`
**(No description)**
```python
<!-- ERROR reading 5ce2fcbee3817b0fb095bc7648371948aad429: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/d2/7a05ecba0213ffdeeab89bb9ad8cc71ba70534`
**(No description)**
```python
<!-- ERROR reading 7a05ecba0213ffdeeab89bb9ad8cc71ba70534: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/d2/bf30b56319ba862c5c9a1a39a87c6d1cb68718`
**(No description)**
```python
<!-- ERROR reading bf30b56319ba862c5c9a1a39a87c6d1cb68718: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/d2/ee13149d34c9882432cdebfec87dff9814076d`
**(No description)**
```python
<!-- ERROR reading ee13149d34c9882432cdebfec87dff9814076d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/d2/fa5ef559160e282839dc85ff6bb43e8eecdcc9`
**(No description)**
```python
<!-- ERROR reading fa5ef559160e282839dc85ff6bb43e8eecdcc9: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/aa/27ce2ffb6c972384db8d65fddaeabd43d3a5f6`
**(No description)**
```python
<!-- ERROR reading 27ce2ffb6c972384db8d65fddaeabd43d3a5f6: 'utf-8' codec can't decode byte 0xdb in position 4: invalid continuation byte -->
```

### `.git/objects/aa/57610040977f323a4e34fdb75181c194ac14a0`
**(No description)**
```python
<!-- ERROR reading 57610040977f323a4e34fdb75181c194ac14a0: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/aa/7431d131213f85ab36cacc54b000e88898080b`
**(No description)**
```python
<!-- ERROR reading 7431d131213f85ab36cacc54b000e88898080b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/aa/cf68f020c7ce7485a20182893f605ee9d06f16`
**(No description)**
```python
<!-- ERROR reading cf68f020c7ce7485a20182893f605ee9d06f16: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/aa/ea748dc5a7566eb5aab6ce08c346286ffb9107`
**(No description)**
```python
<!-- ERROR reading ea748dc5a7566eb5aab6ce08c346286ffb9107: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/aa/fb7aa80ef12f13fa1a8e083f68349ad512cbdd`
**(No description)**
```python
<!-- ERROR reading fb7aa80ef12f13fa1a8e083f68349ad512cbdd: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/af/414697d95473f5c4e2ef26db4e0dc8d9c12d9a`
**(No description)**
```python
<!-- ERROR reading 414697d95473f5c4e2ef26db4e0dc8d9c12d9a: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/af/4a8f3be3242519b529668e321dd8393241f7ea`
**(No description)**
```python
<!-- ERROR reading 4a8f3be3242519b529668e321dd8393241f7ea: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/af/6b970b3025ffe7768809d700f3385279c18c02`
**(No description)**
```python
<!-- ERROR reading 6b970b3025ffe7768809d700f3385279c18c02: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/af/98e75aa7b67c7da9024e5a49e1833a9729036b`
**(No description)**
```python
<!-- ERROR reading 98e75aa7b67c7da9024e5a49e1833a9729036b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/af/acf654b977eb9c0525ea8d29a1d1bd1ec42c6c`
**(No description)**
```python
<!-- ERROR reading acf654b977eb9c0525ea8d29a1d1bd1ec42c6c: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/b7/89f2fa770c9902f8c0761132e5b286cf5e2d60`
**(No description)**
```python
<!-- ERROR reading 89f2fa770c9902f8c0761132e5b286cf5e2d60: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/b7/a06082ae7c34e31f9d4669768c9c6a153612fd`
**(No description)**
```python
<!-- ERROR reading a06082ae7c34e31f9d4669768c9c6a153612fd: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/b7/a3d8e078574e87dc6e345d621f5a596c3bdc1e`
**(No description)**
```python
<!-- ERROR reading a3d8e078574e87dc6e345d621f5a596c3bdc1e: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b7/ae486489756b0429fdb3e9cedc950e3cd0c194`
**(No description)**
```python
<!-- ERROR reading ae486489756b0429fdb3e9cedc950e3cd0c194: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/b7/c42f46736d1f823814e4da1319028ad3d2ffad`
**(No description)**
```python
<!-- ERROR reading c42f46736d1f823814e4da1319028ad3d2ffad: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/b7/e6191abe6b4b10888071e959146e52519bf132`
**(No description)**
```python
<!-- ERROR reading e6191abe6b4b10888071e959146e52519bf132: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/db/173554e2c96156986f025da7c4536baef52185`
**(No description)**
```python
<!-- ERROR reading 173554e2c96156986f025da7c4536baef52185: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/db/554d942f79e2d5ae108e853a6a4a4e6d79c702`
**(No description)**
```python
<!-- ERROR reading 554d942f79e2d5ae108e853a6a4a4e6d79c702: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/db/5a00042e30ade21991a124a9191e30a80f2ffd`
**(No description)**
```python
<!-- ERROR reading 5a00042e30ade21991a124a9191e30a80f2ffd: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/db/a3191e58474c95a66e86ed67b266198f3e7aac`
**(No description)**
```python
<!-- ERROR reading a3191e58474c95a66e86ed67b266198f3e7aac: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/db/d0beeb4da32d8c0175d412fa442eae8f837723`
**(No description)**
```python
<!-- ERROR reading d0beeb4da32d8c0175d412fa442eae8f837723: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/a8/359067ff7afb80e979042077d5fa0fff119ddf`
**(No description)**
```python
<!-- ERROR reading 359067ff7afb80e979042077d5fa0fff119ddf: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/a8/3c4d1026b88bae254d63f11706b39b881577d0`
**(No description)**
```python
<!-- ERROR reading 3c4d1026b88bae254d63f11706b39b881577d0: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/a8/403b7dee407ff18ad4063f98e3645527d1a315`
**(No description)**
```python
<!-- ERROR reading 403b7dee407ff18ad4063f98e3645527d1a315: 'utf-8' codec can't decode byte 0xb1 in position 4: invalid start byte -->
```

### `.git/objects/a8/eaab8a441ac9080f76a539e4289b41a1e3a77b`
**(No description)**
```python
<!-- ERROR reading eaab8a441ac9080f76a539e4289b41a1e3a77b: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/a8/f0e5e59b9567b623cde4547d904dd0e4ac7c1a`
**(No description)**
```python
<!-- ERROR reading f0e5e59b9567b623cde4547d904dd0e4ac7c1a: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/de/1e273ccb43f240da307b39900c12f1834a23fa`
**(No description)**
```python
<!-- ERROR reading 1e273ccb43f240da307b39900c12f1834a23fa: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/de/20dcd38019c2e34c7ef874a28ebbaf3cd59185`
**(No description)**
```python
<!-- ERROR reading 20dcd38019c2e34c7ef874a28ebbaf3cd59185: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/de/297f408d38b2ab5f2deb5e964d3e3c0744c1ed`
**(No description)**
```python
<!-- ERROR reading 297f408d38b2ab5f2deb5e964d3e3c0744c1ed: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/de/91dc8abc88b86fb4186a1a824f684861f04ff5`
**(No description)**
```python
<!-- ERROR reading 91dc8abc88b86fb4186a1a824f684861f04ff5: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/de/98163d739098beec3133269464e28cf76443e1`
**(No description)**
```python
<!-- ERROR reading 98163d739098beec3133269464e28cf76443e1: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/de/9a09a4ed3b078b37e7490a6686f660ae935aca`
**(No description)**
```python
<!-- ERROR reading 9a09a4ed3b078b37e7490a6686f660ae935aca: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/de/d8af87fd91764ec064045bcf785f0780b37b51`
**(No description)**
```python
<!-- ERROR reading d8af87fd91764ec064045bcf785f0780b37b51: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/de/fb20c7c74628435ecbbaf0cbdabdbdd81d8649`
**(No description)**
```python
<!-- ERROR reading fb20c7c74628435ecbbaf0cbdabdbdd81d8649: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/b0/0c6472e1ca70031ca6fa32aa23f04f898971ca`
**(No description)**
```python
<!-- ERROR reading 0c6472e1ca70031ca6fa32aa23f04f898971ca: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/b0/155b18b605326ba0a3104deaefde938b7d651a`
**(No description)**
```python
<!-- ERROR reading 155b18b605326ba0a3104deaefde938b7d651a: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/b0/3971ab4b311d60790dc22ca24d9966426ec0a4`
**(No description)**
```python
<!-- ERROR reading 3971ab4b311d60790dc22ca24d9966426ec0a4: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/b0/85e3d5b033c6ff4c7bbf2e7da3958b6ca5d3ab`
**(No description)**
```python
<!-- ERROR reading 85e3d5b033c6ff4c7bbf2e7da3958b6ca5d3ab: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b0/b06f22f179e91f2d4375ec7239100a4489666e`
**(No description)**
```python
<!-- ERROR reading b06f22f179e91f2d4375ec7239100a4489666e: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/b0/b75d39bf395c036fb0eb5ad032c6d6704853b3`
**(No description)**
```python
<!-- ERROR reading b75d39bf395c036fb0eb5ad032c6d6704853b3: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/b0/bbf78f4367c3e13a5aac0df09b5824d8f7e6ea`
**(No description)**
```python
<!-- ERROR reading bbf78f4367c3e13a5aac0df09b5824d8f7e6ea: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/b0/c89b001fd3b60511734c31e452c1d2053468d0`
**(No description)**
```python
<!-- ERROR reading c89b001fd3b60511734c31e452c1d2053468d0: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/b0/d2b196385e98259971519793447c1fd7a9a643`
**(No description)**
```python
<!-- ERROR reading d2b196385e98259971519793447c1fd7a9a643: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/b0/e1bf49268203d1f9d14cbe73753d95dc66c8a4`
**(No description)**
```python
<!-- ERROR reading e1bf49268203d1f9d14cbe73753d95dc66c8a4: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/a6/024e35e4796ead2004ca5b8ecbf9278f85baa5`
**(No description)**
```python
<!-- ERROR reading 024e35e4796ead2004ca5b8ecbf9278f85baa5: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a6/05c24e58f44175a53b0ac7aec349d57d665ead`
**(No description)**
```python
<!-- ERROR reading 05c24e58f44175a53b0ac7aec349d57d665ead: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/a6/271599f076f28c297aa65ff05873c5ed4e2be8`
**(No description)**
```python
<!-- ERROR reading 271599f076f28c297aa65ff05873c5ed4e2be8: 'utf-8' codec can't decode byte 0xb5 in position 9: invalid start byte -->
```

### `.git/objects/a6/331328d4fbbf4210fcde056654a4248c79b2c7`
**(No description)**
```python
<!-- ERROR reading 331328d4fbbf4210fcde056654a4248c79b2c7: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/a6/57b72e0cbf79be220659576ea6a463e1953fc2`
**(No description)**
```python
<!-- ERROR reading 57b72e0cbf79be220659576ea6a463e1953fc2: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/a6/844dd94b120f080724aa1a5c6bc107d1e2ab85`
**(No description)**
```python
<!-- ERROR reading 844dd94b120f080724aa1a5c6bc107d1e2ab85: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/a6/9165a290f00302c5895e152ff09be07c2ba1ca`
**(No description)**
```python
<!-- ERROR reading 9165a290f00302c5895e152ff09be07c2ba1ca: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/a6/a7be520570a04044497df0da970662962b3c34`
**(No description)**
```python
<!-- ERROR reading a7be520570a04044497df0da970662962b3c34: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/a6/bba14552c7673a7db57a5750ddb06508264273`
**(No description)**
```python
<!-- ERROR reading bba14552c7673a7db57a5750ddb06508264273: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/a6/cdaba84b0c4312da26a4202757cf7f307827bc`
**(No description)**
```python
<!-- ERROR reading cdaba84b0c4312da26a4202757cf7f307827bc: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/b9/2ade52b0dc3867e5c0255c47c64dfd373c854d`
**(No description)**
```python
<!-- ERROR reading 2ade52b0dc3867e5c0255c47c64dfd373c854d: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/b9/66dcea57a2072f98b96dbba75ceb26bd26d2dd`
**(No description)**
```python
<!-- ERROR reading 66dcea57a2072f98b96dbba75ceb26bd26d2dd: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/b9/755545418673fcaa659883eed7ef6c8f8c534f`
**(No description)**
```python
<!-- ERROR reading 755545418673fcaa659883eed7ef6c8f8c534f: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/b9/7d020b634a9f47f5ae6aa3b30e2bd13a6c48c4`
**(No description)**
```python
<!-- ERROR reading 7d020b634a9f47f5ae6aa3b30e2bd13a6c48c4: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/b9/93f008ec476cf0cba9841c1851d5100036ac79`
**(No description)**
```python
<!-- ERROR reading 93f008ec476cf0cba9841c1851d5100036ac79: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/b9/9538a272d985e5288faff04d2e7971b938d613`
**(No description)**
```python
<!-- ERROR reading 9538a272d985e5288faff04d2e7971b938d613: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/b9/a5344aef2962670f9b305a02cd0b11f2087d2f`
**(No description)**
```python
<!-- ERROR reading a5344aef2962670f9b305a02cd0b11f2087d2f: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/b9/c1e3c5ace24a68ebc5806a9f591f65f34ac9d0`
**(No description)**
```python
<!-- ERROR reading c1e3c5ace24a68ebc5806a9f591f65f34ac9d0: 'utf-8' codec can't decode byte 0xc4 in position 3: invalid continuation byte -->
```

### `.git/objects/b9/e2c695c98fb0115679ed9c600248357924e2dc`
**(No description)**
```python
<!-- ERROR reading e2c695c98fb0115679ed9c600248357924e2dc: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/a1/40095e1b8de022f321a41c0125e0e5febc0749`
**(No description)**
```python
<!-- ERROR reading 40095e1b8de022f321a41c0125e0e5febc0749: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/a1/4bec144a97a5e3718a768abe3b6a9e7e93d2c1`
**(No description)**
```python
<!-- ERROR reading 4bec144a97a5e3718a768abe3b6a9e7e93d2c1: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/a1/9b8be03af05a6c16dea41a61529ec714f57bfb`
**(No description)**
```python
<!-- ERROR reading 9b8be03af05a6c16dea41a61529ec714f57bfb: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/a1/a661765d69147fab1299526f2fd3e21a4da2e6`
**(No description)**
```python
<!-- ERROR reading a661765d69147fab1299526f2fd3e21a4da2e6: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/a1/b3b02ff0a94b0611a4ca44345d42a226d15ee5`
**(No description)**
```python
<!-- ERROR reading b3b02ff0a94b0611a4ca44345d42a226d15ee5: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/a1/b589e38a32041e49332e5e81c2d363dc418d68`
**(No description)**
```python
<!-- ERROR reading b589e38a32041e49332e5e81c2d363dc418d68: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/a1/bbbbe3bff592b2bc761772dc6974af4afb7035`
**(No description)**
```python
<!-- ERROR reading bbbbe3bff592b2bc761772dc6974af4afb7035: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/a1/c99a8cb301f222feb1845be4e80d9b1f9d2622`
**(No description)**
```python
<!-- ERROR reading c99a8cb301f222feb1845be4e80d9b1f9d2622: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/a1/f359c3dda8aa4d4b8841c8644bdb56a42357ea`
**(No description)**
```python
<!-- ERROR reading f359c3dda8aa4d4b8841c8644bdb56a42357ea: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/ef/3fde5206524962f0d4fd434d8101abde84bb14`
**(No description)**
```python
<!-- ERROR reading 3fde5206524962f0d4fd434d8101abde84bb14: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/ef/81a780d3e9f07914316901a958cfd2ac816989`
**(No description)**
```python
<!-- ERROR reading 81a780d3e9f07914316901a958cfd2ac816989: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/ef/91df460448239b64ce2ec32f763fb66630daf2`
**(No description)**
```python
<!-- ERROR reading 91df460448239b64ce2ec32f763fb66630daf2: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/ef/9c9683ee8fe971d1101f0ca863719fb1adcbc3`
**(No description)**
```python
<!-- ERROR reading 9c9683ee8fe971d1101f0ca863719fb1adcbc3: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/ef/d793abca4bf496001a4e46a67557e5a6f16bba`
**(No description)**
```python
<!-- ERROR reading d793abca4bf496001a4e46a67557e5a6f16bba: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/c3/0e7c92dc7f1688c86c345b47656b3561d71373`
**(No description)**
```python
<!-- ERROR reading 0e7c92dc7f1688c86c345b47656b3561d71373: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c3/16fd973adf9352c1b3a54f8744387bebe70cee`
**(No description)**
```python
<!-- ERROR reading 16fd973adf9352c1b3a54f8744387bebe70cee: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c3/26e80dd117458ff6e71741ca57359629b05ae4`
**(No description)**
```python
<!-- ERROR reading 26e80dd117458ff6e71741ca57359629b05ae4: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c3/29c767834f73b1dd8991a4ac12d4972a41e98a`
**(No description)**
```python
<!-- ERROR reading 29c767834f73b1dd8991a4ac12d4972a41e98a: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c3/3bebaed26aeead3a97b48dcd4f34308ca3976e`
**(No description)**
```python
<!-- ERROR reading 3bebaed26aeead3a97b48dcd4f34308ca3976e: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/c3/8635471f8dd426b5ff5dfdd29269150b0115ca`
**(No description)**
```python
<!-- ERROR reading 8635471f8dd426b5ff5dfdd29269150b0115ca: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c3/cda1ecda8629edbdca2e3bc04bc51dba5e1430`
**(No description)**
```python
<!-- ERROR reading cda1ecda8629edbdca2e3bc04bc51dba5e1430: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c3/f1657fce94589bd1ec7cead810639047f3d359`
**(No description)**
```python
<!-- ERROR reading f1657fce94589bd1ec7cead810639047f3d359: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/c4/026724cf8d8f1f23eef9a3567e883d2bdd45b8`
**(No description)**
```python
<!-- ERROR reading 026724cf8d8f1f23eef9a3567e883d2bdd45b8: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/c4/2623e9423c23b555d9d352bc5dab518ede02c2`
**(No description)**
```python
<!-- ERROR reading 2623e9423c23b555d9d352bc5dab518ede02c2: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c4/3146279d300ad2b639b5ffb75e41faae561af1`
**(No description)**
```python
<!-- ERROR reading 3146279d300ad2b639b5ffb75e41faae561af1: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/c4/3555deb8ea83b14241a5631c9ea451c96f6e7f`
**(No description)**
```python
<!-- ERROR reading 3555deb8ea83b14241a5631c9ea451c96f6e7f: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/c4/4ff93cb2f572afc6e679308024b744b65c3b0a`
**(No description)**
```python
<!-- ERROR reading 4ff93cb2f572afc6e679308024b744b65c3b0a: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/c4/5258fa03a3ddd6a73db4514365f8741d16ca86`
**(No description)**
```python
<!-- ERROR reading 5258fa03a3ddd6a73db4514365f8741d16ca86: 'utf-8' codec can't decode byte 0xdc in position 6: invalid continuation byte -->
```

### `.git/objects/c4/95e26b72f86ecdcb2db6ebd3a434ab4cc84edb`
**(No description)**
```python
<!-- ERROR reading 95e26b72f86ecdcb2db6ebd3a434ab4cc84edb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c4/c6a797d2675e1c13b028be977c64a822fb649b`
**(No description)**
```python
<!-- ERROR reading c6a797d2675e1c13b028be977c64a822fb649b: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/c4/c85b0388dded43e3e848043563e4d48ea0dbed`
**(No description)**
```python
<!-- ERROR reading c85b0388dded43e3e848043563e4d48ea0dbed: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/c4/eb6b62eb7662329804193a8f9590d06f185be6`
**(No description)**
```python
<!-- ERROR reading eb6b62eb7662329804193a8f9590d06f185be6: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/c4/ec7eb1d0c5fa9c186a2f36454b3bf8bd0df266`
**(No description)**
```python
<!-- ERROR reading ec7eb1d0c5fa9c186a2f36454b3bf8bd0df266: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/ea/1fe42e6d3e0f0044c9b601fa963f9c503ce0ca`
**(No description)**
```python
<!-- ERROR reading 1fe42e6d3e0f0044c9b601fa963f9c503ce0ca: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/ea/92dc301fe3fcf2ec9839c39c7844ae9f5df614`
**(No description)**
```python
<!-- ERROR reading 92dc301fe3fcf2ec9839c39c7844ae9f5df614: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/ea/c22276a34ccd73fc9d70c67ca318a49eb11e77`
**(No description)**
```python
<!-- ERROR reading c22276a34ccd73fc9d70c67ca318a49eb11e77: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/ea/c4e5986578636ad414648e6015e8b7e9f10432`
**(No description)**
```python
<!-- ERROR reading c4e5986578636ad414648e6015e8b7e9f10432: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/ea/e20884c7f9707b525403687c5447a7a353d519`
**(No description)**
```python
<!-- ERROR reading e20884c7f9707b525403687c5447a7a353d519: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/e1/08827fac874bc6d3cb35ced22fe8beabae2240`
**(No description)**
```python
<!-- ERROR reading 08827fac874bc6d3cb35ced22fe8beabae2240: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/e1/2c10d033026f09cf97b81d29555e12aae8c762`
**(No description)**
```python
<!-- ERROR reading 2c10d033026f09cf97b81d29555e12aae8c762: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/e1/98fe780bf5d24f7eba828a28a279d98133361c`
**(No description)**
```python
<!-- ERROR reading 98fe780bf5d24f7eba828a28a279d98133361c: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/e1/d6f01d53b33f0cba9d61b8f7ba2e8c079e101f`
**(No description)**
```python
<!-- ERROR reading d6f01d53b33f0cba9d61b8f7ba2e8c079e101f: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/cd/052fa08e6d7493e92903b6fd4295a0cb1903b8`
**(No description)**
```python
<!-- ERROR reading 052fa08e6d7493e92903b6fd4295a0cb1903b8: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/cd/0b04e6a43c1bb3767dd136a19a9873fa547514`
**(No description)**
```python
<!-- ERROR reading 0b04e6a43c1bb3767dd136a19a9873fa547514: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/cd/1ace784ec7852b83a6e64087d2e292428fa5e7`
**(No description)**
```python
<!-- ERROR reading 1ace784ec7852b83a6e64087d2e292428fa5e7: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/cd/238ad7e5495759cad0723e9611340271d5c3fd`
**(No description)**
```python
<!-- ERROR reading 238ad7e5495759cad0723e9611340271d5c3fd: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/cd/6c54f35f1312fb57abe7c20958e5b3c466b2ae`
**(No description)**
```python
<!-- ERROR reading 6c54f35f1312fb57abe7c20958e5b3c466b2ae: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/cd/a5329341d88812ddf3d5454ee4971eb74c370b`
**(No description)**
```python
<!-- ERROR reading a5329341d88812ddf3d5454ee4971eb74c370b: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/cd/dd78c5ec2a35cf10567416f9577bb4d345b9d5`
**(No description)**
```python
<!-- ERROR reading dd78c5ec2a35cf10567416f9577bb4d345b9d5: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/cc/6f1bd2822ca40c3e96e49dd1fea25b4a6c8082`
**(No description)**
```python
<!-- ERROR reading 6f1bd2822ca40c3e96e49dd1fea25b4a6c8082: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/cc/930ac5ec3fae080c8311fc95de0c51c0b0092b`
**(No description)**
```python
<!-- ERROR reading 930ac5ec3fae080c8311fc95de0c51c0b0092b: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/cc/9d92066e1680576846e46ccdf645a2b1dd5718`
**(No description)**
```python
<!-- ERROR reading 9d92066e1680576846e46ccdf645a2b1dd5718: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/cc/a2e850c4e1c8ff2ad8993778df8206d11beb10`
**(No description)**
```python
<!-- ERROR reading a2e850c4e1c8ff2ad8993778df8206d11beb10: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/cc/bcfe65e385df2649c74ba6ffbfb209e7202bff`
**(No description)**
```python
<!-- ERROR reading bcfe65e385df2649c74ba6ffbfb209e7202bff: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/cc/cab5d57b86352e51cb59df8b023c42a9304d65`
**(No description)**
```python
<!-- ERROR reading cab5d57b86352e51cb59df8b023c42a9304d65: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/e6/305011adf3f7450fa1e9392147e52b8acf2b0c`
**(No description)**
```python
<!-- ERROR reading 305011adf3f7450fa1e9392147e52b8acf2b0c: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/e6/439e9e45897365d5ac6a85a46864c158a225fd`
**(No description)**
```python
<!-- ERROR reading 439e9e45897365d5ac6a85a46864c158a225fd: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/e6/4592ab4f610abb2dc9f017465032bcb2c250a0`
**(No description)**
```python
<!-- ERROR reading 4592ab4f610abb2dc9f017465032bcb2c250a0: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/e6/577ddf805bd3ce654b15154ec8474959cc1e99`
**(No description)**
```python
<!-- ERROR reading 577ddf805bd3ce654b15154ec8474959cc1e99: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/e6/73d4cc1b1dd7e7ecdbde91fd6ada386c3de03f`
**(No description)**
```python
<!-- ERROR reading 73d4cc1b1dd7e7ecdbde91fd6ada386c3de03f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391`
**(No description)**
```python
<!-- ERROR reading 9de29bb2d1d6434b8b29ae775ad8c2e48c5391: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/e6/ae4e4602b9f7efb1d83f5385fba3bb3b1dcc0f`
**(No description)**
```python
<!-- ERROR reading ae4e4602b9f7efb1d83f5385fba3bb3b1dcc0f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/e6/b1609f7babcd4439376c0d826978f7a66dfa3f`
**(No description)**
```python
<!-- ERROR reading b1609f7babcd4439376c0d826978f7a66dfa3f: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/e6/d6d709852b137a862cfe2b3af42dc790fa705d`
**(No description)**
```python
<!-- ERROR reading d6d709852b137a862cfe2b3af42dc790fa705d: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/e6/ffd3d782dbe876b435acbcd4cc31c0bfe0089f`
**(No description)**
```python
<!-- ERROR reading ffd3d782dbe876b435acbcd4cc31c0bfe0089f: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/f9/0ca8da2a3d3952c6600310765f815df133a9e6`
**(No description)**
```python
<!-- ERROR reading 0ca8da2a3d3952c6600310765f815df133a9e6: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/f9/412a7a9cb8a69b52e4897db43fa91fb3de330b`
**(No description)**
```python
<!-- ERROR reading 412a7a9cb8a69b52e4897db43fa91fb3de330b: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/f9/a081c4f6881cb70633479f8f8fdf21e2cb6d91`
**(No description)**
```python
<!-- ERROR reading a081c4f6881cb70633479f8f8fdf21e2cb6d91: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/f9/f7b2b2944e045a63aded2db0abc9c69a8aa74b`
**(No description)**
```python
<!-- ERROR reading f7b2b2944e045a63aded2db0abc9c69a8aa74b: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/f0/035f0c393a29e89243546a89a4cf62fba2348a`
**(No description)**
```python
<!-- ERROR reading 035f0c393a29e89243546a89a4cf62fba2348a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f0/37759f42e74a88bb685679d2c3f574d186521e`
**(No description)**
```python
<!-- ERROR reading 37759f42e74a88bb685679d2c3f574d186521e: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/f0/3ce6e6d02af7f380a09af7681129a8dd66ec6c`
**(No description)**
```python
<!-- ERROR reading 3ce6e6d02af7f380a09af7681129a8dd66ec6c: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/f0/64d60c8b9ed89d4c8546532caade8d18286f37`
**(No description)**
```python
<!-- ERROR reading 64d60c8b9ed89d4c8546532caade8d18286f37: 'utf-8' codec can't decode byte 0xc2 in position 6: invalid continuation byte -->
```

### `.git/objects/f0/83e51a604c9d8ac74e20b9964ba22fc68ad8ac`
**(No description)**
```python
<!-- ERROR reading 83e51a604c9d8ac74e20b9964ba22fc68ad8ac: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f0/b22ef194ddae262ad59ba7a8d61bedea25f774`
**(No description)**
```python
<!-- ERROR reading b22ef194ddae262ad59ba7a8d61bedea25f774: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/f0/d6b5b8cd8ab3ceb772a6e9f962bbce0bc8c1d2`
**(No description)**
```python
<!-- ERROR reading d6b5b8cd8ab3ceb772a6e9f962bbce0bc8c1d2: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/f0/e6712d3172f4dc3e26d4e080cc9a643dc18a9d`
**(No description)**
```python
<!-- ERROR reading e6712d3172f4dc3e26d4e080cc9a643dc18a9d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f7/56f9dd4a7393db54db796ac18118d65fc18a3b`
**(No description)**
```python
<!-- ERROR reading 56f9dd4a7393db54db796ac18118d65fc18a3b: 'utf-8' codec can't decode byte 0xb6 in position 9: invalid start byte -->
```

### `.git/objects/f7/7520ee106deeedee30a48005479806ff9a19e2`
**(No description)**
```python
<!-- ERROR reading 7520ee106deeedee30a48005479806ff9a19e2: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/f7/9f7bc813d088a77254b83ff58a377c734af640`
**(No description)**
```python
<!-- ERROR reading 9f7bc813d088a77254b83ff58a377c734af640: 'utf-8' codec can't decode byte 0xf1 in position 21: invalid continuation byte -->
```

### `.git/objects/f7/ab32cfe1d1515f72d8204502beba59c350fda6`
**(No description)**
```python
<!-- ERROR reading ab32cfe1d1515f72d8204502beba59c350fda6: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/f7/dbf4c9aa8314816f9bcbe5357146369ee71391`
**(No description)**
```python
<!-- ERROR reading dbf4c9aa8314816f9bcbe5357146369ee71391: 'utf-8' codec can't decode byte 0xcb in position 4: invalid continuation byte -->
```

### `.git/objects/e8/4e65e3e14152a2ba6e6e05d914f0e1bbef187b`
**(No description)**
```python
<!-- ERROR reading 4e65e3e14152a2ba6e6e05d914f0e1bbef187b: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/e8/59590f886cd78344206af1a8ccb3080d4385e0`
**(No description)**
```python
<!-- ERROR reading 59590f886cd78344206af1a8ccb3080d4385e0: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/e8/795ed35c598d9635961bac628c4129b83844b7`
**(No description)**
```python
<!-- ERROR reading 795ed35c598d9635961bac628c4129b83844b7: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/e8/97029c34c2692e24c62eab90b732864d997b63`
**(No description)**
```python
<!-- ERROR reading 97029c34c2692e24c62eab90b732864d997b63: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/e8/ae5e4beaa287c8bcb31c77d8f3f2e4565bba60`
**(No description)**
```python
<!-- ERROR reading ae5e4beaa287c8bcb31c77d8f3f2e4565bba60: 'utf-8' codec can't decode byte 0x99 in position 3: invalid start byte -->
```

### `.git/objects/e8/ebee957f446f81816a2764d8c30d808117e4cd`
**(No description)**
```python
<!-- ERROR reading ebee957f446f81816a2764d8c30d808117e4cd: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/fa/1b07f9d4ae40d53270ddc23eb7ae9e69ab1d59`
**(No description)**
```python
<!-- ERROR reading 1b07f9d4ae40d53270ddc23eb7ae9e69ab1d59: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/fa/6458dff168bb33c1f759da9fe7e71b2f0f9f9c`
**(No description)**
```python
<!-- ERROR reading 6458dff168bb33c1f759da9fe7e71b2f0f9f9c: 'utf-8' codec can't decode byte 0xaa in position 6: invalid start byte -->
```

### `.git/objects/fa/7a450b74e813e66fd6e9a140d48c29215503bb`
**(No description)**
```python
<!-- ERROR reading 7a450b74e813e66fd6e9a140d48c29215503bb: 'utf-8' codec can't decode byte 0xc2 in position 6: invalid continuation byte -->
```

### `.git/objects/fa/89c83efcdad1f5c81a4b35bbb64ea64ea6101f`
**(No description)**
```python
<!-- ERROR reading 89c83efcdad1f5c81a4b35bbb64ea64ea6101f: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/fa/aae405921bf8427f1132c263e3cb4cbc192f55`
**(No description)**
```python
<!-- ERROR reading aae405921bf8427f1132c263e3cb4cbc192f55: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/fa/aae9a8ddba9a7bc25302fa08ffb88e86628006`
**(No description)**
```python
<!-- ERROR reading aae9a8ddba9a7bc25302fa08ffb88e86628006: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/fa/cfa0dd249f67ca6abd39ff2ae04d6912d5fc61`
**(No description)**
```python
<!-- ERROR reading cfa0dd249f67ca6abd39ff2ae04d6912d5fc61: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/fa/efaf003750294984d8fb44915b3ae56c2c4cc9`
**(No description)**
```python
<!-- ERROR reading efaf003750294984d8fb44915b3ae56c2c4cc9: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ff/5efbcab3b58063dd84787181c26a95fb663d94`
**(No description)**
```python
<!-- ERROR reading 5efbcab3b58063dd84787181c26a95fb663d94: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/ff/69593b05b5eb5fcd336b4bd16193c44dc48ef5`
**(No description)**
```python
<!-- ERROR reading 69593b05b5eb5fcd336b4bd16193c44dc48ef5: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/ff/d6233c2432da169ecd4a4b9a00f4d7f05d9e98`
**(No description)**
```python
<!-- ERROR reading d6233c2432da169ecd4a4b9a00f4d7f05d9e98: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/c5/05464f6355424f9109147423730130595077a5`
**(No description)**
```python
<!-- ERROR reading 05464f6355424f9109147423730130595077a5: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/c5/07da360aa3d9ccff7a6ed0249ddf03df521c39`
**(No description)**
```python
<!-- ERROR reading 07da360aa3d9ccff7a6ed0249ddf03df521c39: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/c5/5d408b6b1df7f68745e43393a1200a02b6b7ec`
**(No description)**
```python
<!-- ERROR reading 5d408b6b1df7f68745e43393a1200a02b6b7ec: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/c5/65007eec77e516f364de0dc2e47fdc09c4c404`
**(No description)**
```python
<!-- ERROR reading 65007eec77e516f364de0dc2e47fdc09c4c404: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/c5/6af390fe250c1048036375fff340db5d2807a8`
**(No description)**
```python
<!-- ERROR reading 6af390fe250c1048036375fff340db5d2807a8: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/c5/6b2ffcceaad63cb853229f04bf2f9a684c666e`
**(No description)**
```python
<!-- ERROR reading 6b2ffcceaad63cb853229f04bf2f9a684c666e: 'utf-8' codec can't decode byte 0xbb in position 4: invalid start byte -->
```

### `.git/objects/c5/90627eaa0a12a063bd2eb8a84e2935e11f6e71`
**(No description)**
```python
<!-- ERROR reading 90627eaa0a12a063bd2eb8a84e2935e11f6e71: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/c5/9eff8bbf7bf9f3ec79e9f2ffbc426e2233df5c`
**(No description)**
```python
<!-- ERROR reading 9eff8bbf7bf9f3ec79e9f2ffbc426e2233df5c: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c5/a0699dd96e551f9dc7083162e8a304b10716b0`
**(No description)**
```python
<!-- ERROR reading a0699dd96e551f9dc7083162e8a304b10716b0: 'utf-8' codec can't decode bytes in position 5-6: invalid continuation byte -->
```

### `.git/objects/c5/b0a5178b1fb0ae6ef08c2fe753433820390a31`
**(No description)**
```python
<!-- ERROR reading b0a5178b1fb0ae6ef08c2fe753433820390a31: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/c2/2a8d09d27a2d57b385e62def0adb3590e3af1b`
**(No description)**
```python
<!-- ERROR reading 2a8d09d27a2d57b385e62def0adb3590e3af1b: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/c2/53bc7f2647e9112939d36b3db8ea98c0d18827`
**(No description)**
```python
<!-- ERROR reading 53bc7f2647e9112939d36b3db8ea98c0d18827: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/c2/5770890138e5f8743f8e127bbbbb32a3184a7d`
**(No description)**
```python
<!-- ERROR reading 5770890138e5f8743f8e127bbbbb32a3184a7d: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/c2/80646c7be0b1887878254408c6f6c5158651ca`
**(No description)**
```python
<!-- ERROR reading 80646c7be0b1887878254408c6f6c5158651ca: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/c2/a9d8c2a4fc22209b0b35dbc904899c347ea7a6`
**(No description)**
```python
<!-- ERROR reading a9d8c2a4fc22209b0b35dbc904899c347ea7a6: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/c2/c6562c734782bcf5eb011b74788b8405478d89`
**(No description)**
```python
<!-- ERROR reading c6562c734782bcf5eb011b74788b8405478d89: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/c2/c988530b4fa52af441381a13888532478e8038`
**(No description)**
```python
<!-- ERROR reading c988530b4fa52af441381a13888532478e8038: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/c2/d836033673993e00a02d5a3802b61cd051cf08`
**(No description)**
```python
<!-- ERROR reading d836033673993e00a02d5a3802b61cd051cf08: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/c2/ec358d2fed946d19b47dc02560e1a79819dd12`
**(No description)**
```python
<!-- ERROR reading ec358d2fed946d19b47dc02560e1a79819dd12: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f6/1ed7873dde7db1979fe10fe54218a81f710360`
**(No description)**
```python
<!-- ERROR reading 1ed7873dde7db1979fe10fe54218a81f710360: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/f6/955b0dccdca0bec9827c0a76d7246c155fce3a`
**(No description)**
```python
<!-- ERROR reading 955b0dccdca0bec9827c0a76d7246c155fce3a: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f6/99839e82d21316fc7b2fc805b6c71a16f99760`
**(No description)**
```python
<!-- ERROR reading 99839e82d21316fc7b2fc805b6c71a16f99760: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/f6/e5c40c7ff2a878d4ce7a37364b6d93974b8ee8`
**(No description)**
```python
<!-- ERROR reading e5c40c7ff2a878d4ce7a37364b6d93974b8ee8: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/e9/04a83d4859eec2405a1b554d6f2bf55d291ca2`
**(No description)**
```python
<!-- ERROR reading 04a83d4859eec2405a1b554d6f2bf55d291ca2: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/e9/3adec99e73b4cc7eddef6c9befa8866b5013bd`
**(No description)**
```python
<!-- ERROR reading 3adec99e73b4cc7eddef6c9befa8866b5013bd: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/e9/63a50979a0b3dd56558240e075ca0f889479df`
**(No description)**
```python
<!-- ERROR reading 63a50979a0b3dd56558240e075ca0f889479df: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/e9/8902dfadb02648eacf57fbdafa297abeed1177`
**(No description)**
```python
<!-- ERROR reading 8902dfadb02648eacf57fbdafa297abeed1177: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/e9/a7995c112c33eb07cfafeea46dba15bc847631`
**(No description)**
```python
<!-- ERROR reading a7995c112c33eb07cfafeea46dba15bc847631: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/e9/addde071f81758baf350c4ab6bde2556340131`
**(No description)**
```python
<!-- ERROR reading addde071f81758baf350c4ab6bde2556340131: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/f1/1d97b541eff68a5c3654ab15b6becb3e861697`
**(No description)**
```python
<!-- ERROR reading 1d97b541eff68a5c3654ab15b6becb3e861697: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f1/a11278e3ddfa6aed3fc0c731084c6b22d89e0d`
**(No description)**
```python
<!-- ERROR reading a11278e3ddfa6aed3fc0c731084c6b22d89e0d: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f1/ac051dab21bacf3f557bd495dadf209daec455`
**(No description)**
```python
<!-- ERROR reading ac051dab21bacf3f557bd495dadf209daec455: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f1/c0f06337053716d57a9e64d6e46f42bd14abda`
**(No description)**
```python
<!-- ERROR reading c0f06337053716d57a9e64d6e46f42bd14abda: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/f1/c38e390cf2fd246b7fc85ca41ef91aff3daec6`
**(No description)**
```python
<!-- ERROR reading c38e390cf2fd246b7fc85ca41ef91aff3daec6: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f1/e0ad94a1ce2cd06bf381845fafbecbd9846f88`
**(No description)**
```python
<!-- ERROR reading e0ad94a1ce2cd06bf381845fafbecbd9846f88: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/e7/0d692c85a13872f7d87bc12b6ab82ea99e429b`
**(No description)**
```python
<!-- ERROR reading 0d692c85a13872f7d87bc12b6ab82ea99e429b: 'utf-8' codec can't decode byte 0xc4 in position 6: invalid continuation byte -->
```

### `.git/objects/e7/14a6f80394379faf66ec9dca10c82de8e687b0`
**(No description)**
```python
<!-- ERROR reading 14a6f80394379faf66ec9dca10c82de8e687b0: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/e7/3ad209ae86b26d6fa892f1eba39cfc28980970`
**(No description)**
```python
<!-- ERROR reading 3ad209ae86b26d6fa892f1eba39cfc28980970: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/e7/65af2c2dd5aedd711aae5e3420d19634ce9eca`
**(No description)**
```python
<!-- ERROR reading 65af2c2dd5aedd711aae5e3420d19634ce9eca: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/e7/f30f491b897e66597cf403a8959e3e7bb955a8`
**(No description)**
```python
<!-- ERROR reading f30f491b897e66597cf403a8959e3e7bb955a8: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/e7/fd344aad3fc4d9be528c12ea10b20cf6e768bb`
**(No description)**
```python
<!-- ERROR reading fd344aad3fc4d9be528c12ea10b20cf6e768bb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/cb/1ce8772af26eac21dc4934dbabfcc1ecba16ce`
**(No description)**
```python
<!-- ERROR reading 1ce8772af26eac21dc4934dbabfcc1ecba16ce: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/cb/977cff9545ef5d48ad7cf13f2cbe1ebc3e7cd0`
**(No description)**
```python
<!-- ERROR reading 977cff9545ef5d48ad7cf13f2cbe1ebc3e7cd0: 'utf-8' codec can't decode byte 0xf4 in position 9: invalid continuation byte -->
```

### `.git/objects/cb/a6f3f560f71b3b15ab6aaf21dde4f1bba1bd00`
**(No description)**
```python
<!-- ERROR reading a6f3f560f71b3b15ab6aaf21dde4f1bba1bd00: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/f8/9afaf433c443b16f67c9e68e0b87d49a87db04`
**(No description)**
```python
<!-- ERROR reading 9afaf433c443b16f67c9e68e0b87d49a87db04: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/f8/aee0466a23b9fc3dc36c6e80c39e6a826a7753`
**(No description)**
```python
<!-- ERROR reading aee0466a23b9fc3dc36c6e80c39e6a826a7753: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/f8/b780e1911115cf87474c7a81c8b362519addcb`
**(No description)**
```python
<!-- ERROR reading b780e1911115cf87474c7a81c8b362519addcb: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/f8/d3509653ba8f80ca7f3aa7f95616142ba83a94`
**(No description)**
```python
<!-- ERROR reading d3509653ba8f80ca7f3aa7f95616142ba83a94: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/f8/d43bb13cedecc52f4f43e2d68d680ec526fcf3`
**(No description)**
```python
<!-- ERROR reading d43bb13cedecc52f4f43e2d68d680ec526fcf3: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/ce/0564ceac8aac425675b5c8f7f7205d08061fd3`
**(No description)**
```python
<!-- ERROR reading 0564ceac8aac425675b5c8f7f7205d08061fd3: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/ce/0a19ee26408e45437e971cf129318fbcf44acd`
**(No description)**
```python
<!-- ERROR reading 0a19ee26408e45437e971cf129318fbcf44acd: 'utf-8' codec can't decode byte 0x8c in position 3: invalid start byte -->
```

### `.git/objects/ce/27bf335f1f4cbe8912fd7db62cdf99f68fcc93`
**(No description)**
```python
<!-- ERROR reading 27bf335f1f4cbe8912fd7db62cdf99f68fcc93: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/ce/4c990b810351ef5fce67f7b2e6ff47bb5ddf7b`
**(No description)**
```python
<!-- ERROR reading 4c990b810351ef5fce67f7b2e6ff47bb5ddf7b: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/ce/66bd4addbde1e332e9a42f6eb62adc471193e5`
**(No description)**
```python
<!-- ERROR reading 66bd4addbde1e332e9a42f6eb62adc471193e5: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/ce/95fec78fcc8223195a82000b854365d3d76171`
**(No description)**
```python
<!-- ERROR reading 95fec78fcc8223195a82000b854365d3d76171: 'utf-8' codec can't decode byte 0xb1 in position 9: invalid start byte -->
```

### `.git/objects/ce/e70e332f9802a5963bfed8149ac997e5b30de2`
**(No description)**
```python
<!-- ERROR reading e70e332f9802a5963bfed8149ac997e5b30de2: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/e0/58e2c65734c1aa4bb8dab54ce6f0211170cfd8`
**(No description)**
```python
<!-- ERROR reading 58e2c65734c1aa4bb8dab54ce6f0211170cfd8: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/e0/624ba9b5ab13592c557b549bb3f5c5a45762d6`
**(No description)**
```python
<!-- ERROR reading 624ba9b5ab13592c557b549bb3f5c5a45762d6: 'utf-8' codec can't decode byte 0xb5 in position 10: invalid start byte -->
```

### `.git/objects/e0/70f6815396e3183b85007aff34c6f628418ead`
**(No description)**
```python
<!-- ERROR reading 70f6815396e3183b85007aff34c6f628418ead: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/e0/96d1d52dd1a608f8ae3c814d877f01dbf5fda8`
**(No description)**
```python
<!-- ERROR reading 96d1d52dd1a608f8ae3c814d877f01dbf5fda8: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/e0/995ea07d2686f6838e06cceede82b26928a656`
**(No description)**
```python
<!-- ERROR reading 995ea07d2686f6838e06cceede82b26928a656: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/e0/9d751eca3ec385ba20b9555a768730eb80174b`
**(No description)**
```python
<!-- ERROR reading 9d751eca3ec385ba20b9555a768730eb80174b: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/e0/bb37602c8e2f1f808ba8fdcb1b7f63451fa4f5`
**(No description)**
```python
<!-- ERROR reading bb37602c8e2f1f808ba8fdcb1b7f63451fa4f5: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/e0/f8d9daa286b23fa37e96d95d6b4a4d64c8f430`
**(No description)**
```python
<!-- ERROR reading f8d9daa286b23fa37e96d95d6b4a4d64c8f430: 'utf-8' codec can't decode byte 0xd4 in position 6: invalid continuation byte -->
```

### `.git/objects/46/139dbf9400b7bc0b64e6756ce17b4eb5fd7436`
**(No description)**
```python
<!-- ERROR reading 139dbf9400b7bc0b64e6756ce17b4eb5fd7436: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/46/3d8a7bc3ff374b474f6cb3421b7dbe8a095ef6`
**(No description)**
```python
<!-- ERROR reading 3d8a7bc3ff374b474f6cb3421b7dbe8a095ef6: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/46/3dd88259cdc9a8a289f03e930db5e3ca01c059`
**(No description)**
```python
<!-- ERROR reading 3dd88259cdc9a8a289f03e930db5e3ca01c059: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/46/7a6c90ae269babe3af7963d9d7c78b9f012268`
**(No description)**
```python
<!-- ERROR reading 7a6c90ae269babe3af7963d9d7c78b9f012268: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/46/8c3cd7340bcfa79e3379981ba56e30da46d695`
**(No description)**
```python
<!-- ERROR reading 8c3cd7340bcfa79e3379981ba56e30da46d695: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/46/ba835c66c9f4c3b15b0a0671447d33b3b240d1`
**(No description)**
```python
<!-- ERROR reading ba835c66c9f4c3b15b0a0671447d33b3b240d1: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/46/eb1724e35acc50120469cd7bc5c1bc4ab9416d`
**(No description)**
```python
<!-- ERROR reading eb1724e35acc50120469cd7bc5c1bc4ab9416d: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/46/f4b2846fd708ecb81b2d665434ce6379aa1101`
**(No description)**
```python
<!-- ERROR reading f4b2846fd708ecb81b2d665434ce6379aa1101: 'utf-8' codec can't decode byte 0xdd in position 4: invalid continuation byte -->
```

### `.git/objects/2c/22dde77e872ed4f28c807f318c0070c6b22c14`
**(No description)**
```python
<!-- ERROR reading 22dde77e872ed4f28c807f318c0070c6b22c14: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/2c/2fd860af40b0fe876fa5932d930b1ba86f0069`
**(No description)**
```python
<!-- ERROR reading 2fd860af40b0fe876fa5932d930b1ba86f0069: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/2c/7c2c2ffdb45ca50cd2b7e57bde1fc711adb851`
**(No description)**
```python
<!-- ERROR reading 7c2c2ffdb45ca50cd2b7e57bde1fc711adb851: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/2c/c433a4a55e3b41fa31089918fb62096092f89f`
**(No description)**
```python
<!-- ERROR reading c433a4a55e3b41fa31089918fb62096092f89f: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/79/1fc15b0d3f4eaca9982e92045b3ecfe0c3833a`
**(No description)**
```python
<!-- ERROR reading 1fc15b0d3f4eaca9982e92045b3ecfe0c3833a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/79/21b04f05d5ef0ad20365e7372a48d86724dc51`
**(No description)**
```python
<!-- ERROR reading 21b04f05d5ef0ad20365e7372a48d86724dc51: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/79/b2e7f38c1c07472dd8dd968b4e9b4de5422d76`
**(No description)**
```python
<!-- ERROR reading b2e7f38c1c07472dd8dd968b4e9b4de5422d76: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/79/bc095185c79313b238fb034ef746c7f67b9d93`
**(No description)**
```python
<!-- ERROR reading bc095185c79313b238fb034ef746c7f67b9d93: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/2d/03437bb1c41915f0faf610b8a1fc54637e74fd`
**(No description)**
```python
<!-- ERROR reading 03437bb1c41915f0faf610b8a1fc54637e74fd: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/2d/1b5fa2d3366fd6584181a26c8569a0207900cc`
**(No description)**
```python
<!-- ERROR reading 1b5fa2d3366fd6584181a26c8569a0207900cc: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/2d/1c999e25f40929aacd526ad8b737bbd6394e1f`
**(No description)**
```python
<!-- ERROR reading 1c999e25f40929aacd526ad8b737bbd6394e1f: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/2d/447b857d34c8e8ed1e16b48e7d1d6a7e5c293a`
**(No description)**
```python
<!-- ERROR reading 447b857d34c8e8ed1e16b48e7d1d6a7e5c293a: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/2d/65058ff7bb13e4cd00c0be8cf8c645eca7f4a9`
**(No description)**
```python
<!-- ERROR reading 65058ff7bb13e4cd00c0be8cf8c645eca7f4a9: 'utf-8' codec can't decode byte 0xb2 in position 9: invalid start byte -->
```

### `.git/objects/2d/697b0d7219c58fa370de4c2eeca04e0afed575`
**(No description)**
```python
<!-- ERROR reading 697b0d7219c58fa370de4c2eeca04e0afed575: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/2d/915e6fcecbf920e3ab43f7a2eab667b6736ce5`
**(No description)**
```python
<!-- ERROR reading 915e6fcecbf920e3ab43f7a2eab667b6736ce5: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/2d/adb5aefde5416bb62ea65cb93556cba476a752`
**(No description)**
```python
<!-- ERROR reading adb5aefde5416bb62ea65cb93556cba476a752: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/2d/fe321e9686154c989d6a4a7b4c7db8c303759a`
**(No description)**
```python
<!-- ERROR reading fe321e9686154c989d6a4a7b4c7db8c303759a: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/2d/fff809fc477b9652e9072913da912dd92a5d07`
**(No description)**
```python
<!-- ERROR reading fff809fc477b9652e9072913da912dd92a5d07: 'utf-8' codec can't decode byte 0x85 in position 15: invalid start byte -->
```

### `.git/objects/41/243ba53c2249006e4869b322f61d505bfbdae0`
**(No description)**
```python
<!-- ERROR reading 243ba53c2249006e4869b322f61d505bfbdae0: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/41/29bf7e14c4da72a7b518c9611327be067e6540`
**(No description)**
```python
<!-- ERROR reading 29bf7e14c4da72a7b518c9611327be067e6540: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/41/784104ee4bd5796006d1052536325d52db1e8c`
**(No description)**
```python
<!-- ERROR reading 784104ee4bd5796006d1052536325d52db1e8c: 'utf-8' codec can't decode byte 0xc3 in position 6: invalid continuation byte -->
```

### `.git/objects/41/8c117259aa31de5c9d9bf6a4e5cfcbb5dab2d8`
**(No description)**
```python
<!-- ERROR reading 8c117259aa31de5c9d9bf6a4e5cfcbb5dab2d8: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/41/9734f2a2d5eb52a6ca5bad85320dac55d99d09`
**(No description)**
```python
<!-- ERROR reading 9734f2a2d5eb52a6ca5bad85320dac55d99d09: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/41/a8fd174cbc556d495aca1d58af8e2197ace913`
**(No description)**
```python
<!-- ERROR reading a8fd174cbc556d495aca1d58af8e2197ace913: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/41/c0f3e24cc8ce70021e07749dafb66ca924b4fc`
**(No description)**
```python
<!-- ERROR reading c0f3e24cc8ce70021e07749dafb66ca924b4fc: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/41/c9323cdc73a397cc5a53a0644f81a58715e311`
**(No description)**
```python
<!-- ERROR reading c9323cdc73a397cc5a53a0644f81a58715e311: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/41/d0d5fcae0d946401c2d089b69143f540618b90`
**(No description)**
```python
<!-- ERROR reading d0d5fcae0d946401c2d089b69143f540618b90: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/41/d587da13d4444f62ea8ae54b46d66b4d97402d`
**(No description)**
```python
<!-- ERROR reading d587da13d4444f62ea8ae54b46d66b4d97402d: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/83/60d0f284ef394f2980b5bb89548e234385cdf1`
**(No description)**
```python
<!-- ERROR reading 60d0f284ef394f2980b5bb89548e234385cdf1: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/83/6c6f21a09c948897ed8a34e46aaedc6710b134`
**(No description)**
```python
<!-- ERROR reading 6c6f21a09c948897ed8a34e46aaedc6710b134: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/83/7b27ec486924eb9ccef53c6a5d578bd787aefd`
**(No description)**
```python
<!-- ERROR reading 7b27ec486924eb9ccef53c6a5d578bd787aefd: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/83/bf1d9786b60918115dffcaed50576f57d2494b`
**(No description)**
```python
<!-- ERROR reading bf1d9786b60918115dffcaed50576f57d2494b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/83/d1a5799d041415db71324af0478bc06599dda2`
**(No description)**
```python
<!-- ERROR reading d1a5799d041415db71324af0478bc06599dda2: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/83/f2562b1b117fbeda087edadeb97b314c8b70ce`
**(No description)**
```python
<!-- ERROR reading f2562b1b117fbeda087edadeb97b314c8b70ce: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/83/fc082b545106d02622de20f2083e8a7562f96c`
**(No description)**
```python
<!-- ERROR reading fc082b545106d02622de20f2083e8a7562f96c: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/1b/0dc125f196fbdb855bc0f45724a71355cedd51`
**(No description)**
```python
<!-- ERROR reading 0dc125f196fbdb855bc0f45724a71355cedd51: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/1b/236efdc9b3196a0e3238306b627c03fee69fa1`
**(No description)**
```python
<!-- ERROR reading 236efdc9b3196a0e3238306b627c03fee69fa1: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/1b/66c334139bd9615145d2b09de65e946045f001`
**(No description)**
```python
<!-- ERROR reading 66c334139bd9615145d2b09de65e946045f001: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/1b/931295c8db72ef9856976f57fd7be2e5549b7d`
**(No description)**
```python
<!-- ERROR reading 931295c8db72ef9856976f57fd7be2e5549b7d: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/1b/b3922b7127f95b9a1f365991bb6af5bb873706`
**(No description)**
```python
<!-- ERROR reading b3922b7127f95b9a1f365991bb6af5bb873706: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/1b/ddc2fd4e05d24b196ddd722786108d5183d8e1`
**(No description)**
```python
<!-- ERROR reading ddc2fd4e05d24b196ddd722786108d5183d8e1: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/1b/ead4a061cc0989ffcd999ffeb0a7279ec25b4f`
**(No description)**
```python
<!-- ERROR reading ead4a061cc0989ffcd999ffeb0a7279ec25b4f: 'utf-8' codec can't decode byte 0x85 in position 6: invalid start byte -->
```

### `.git/objects/1b/ecc5093c5ab8e196bb9fee415e2381e7158fc3`
**(No description)**
```python
<!-- ERROR reading ecc5093c5ab8e196bb9fee415e2381e7158fc3: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/77/0bd881baf358582d310e090147efe5d82d3a1c`
**(No description)**
```python
<!-- ERROR reading 0bd881baf358582d310e090147efe5d82d3a1c: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/77/19a3d8640029757fd9a128d5dd6b3c9ccfad91`
**(No description)**
```python
<!-- ERROR reading 19a3d8640029757fd9a128d5dd6b3c9ccfad91: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/77/21c5e058d439448156ddf6bc23f7ccf60a56b9`
**(No description)**
```python
<!-- ERROR reading 21c5e058d439448156ddf6bc23f7ccf60a56b9: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/77/2b2159ccd95d29d8d940fc818d3bb1d2610cbf`
**(No description)**
```python
<!-- ERROR reading 2b2159ccd95d29d8d940fc818d3bb1d2610cbf: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/77/3452d0a6b85b2dfec002c0bbe45d31fb5cd655`
**(No description)**
```python
<!-- ERROR reading 3452d0a6b85b2dfec002c0bbe45d31fb5cd655: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/77/7268c3baa8a64e03cab9cf8a4a62881374ce0d`
**(No description)**
```python
<!-- ERROR reading 7268c3baa8a64e03cab9cf8a4a62881374ce0d: 'utf-8' codec can't decode byte 0xaa in position 6: invalid start byte -->
```

### `.git/objects/77/8805f5a5435bd45ca94f4a60241185e775dc8e`
**(No description)**
```python
<!-- ERROR reading 8805f5a5435bd45ca94f4a60241185e775dc8e: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/77/a025a0e9a53e72a12d9783914fa4180fdd73e6`
**(No description)**
```python
<!-- ERROR reading a025a0e9a53e72a12d9783914fa4180fdd73e6: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/77/a2de2004163a3829291ba844a132d766d0a912`
**(No description)**
```python
<!-- ERROR reading a2de2004163a3829291ba844a132d766d0a912: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/77/a8b9185a07d0338e652810f48757dfe9e0c90c`
**(No description)**
```python
<!-- ERROR reading a8b9185a07d0338e652810f48757dfe9e0c90c: 'utf-8' codec can't decode byte 0x8b in position 5: invalid start byte -->
```

### `.git/objects/77/b67fc8ff7047bdf6ce604d7f667f92fc62f4bf`
**(No description)**
```python
<!-- ERROR reading b67fc8ff7047bdf6ce604d7f667f92fc62f4bf: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/77/cbf773e237a6ecab941ecdd68f685e4f06bf06`
**(No description)**
```python
<!-- ERROR reading cbf773e237a6ecab941ecdd68f685e4f06bf06: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/77/f45a6d3986d15626fc8a5fd459d6a3e0fbe466`
**(No description)**
```python
<!-- ERROR reading f45a6d3986d15626fc8a5fd459d6a3e0fbe466: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/77/fd77cdf4e5c0fa81db80315e314c91d7b0269a`
**(No description)**
```python
<!-- ERROR reading fd77cdf4e5c0fa81db80315e314c91d7b0269a: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/48/1eea9fd4b5a5ca67e75bc9d3b3effe6ce29194`
**(No description)**
```python
<!-- ERROR reading 1eea9fd4b5a5ca67e75bc9d3b3effe6ce29194: 'utf-8' codec can't decode byte 0x92 in position 3: invalid start byte -->
```

### `.git/objects/48/22d166551d986bfbc254c0972657cba2a6d883`
**(No description)**
```python
<!-- ERROR reading 22d166551d986bfbc254c0972657cba2a6d883: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/48/4c652a48e0c97826acabfc475d1bab7ea4763a`
**(No description)**
```python
<!-- ERROR reading 4c652a48e0c97826acabfc475d1bab7ea4763a: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/48/6be6f8e1fab8f83b70b58d1914fff0ea12625f`
**(No description)**
```python
<!-- ERROR reading 6be6f8e1fab8f83b70b58d1914fff0ea12625f: 'utf-8' codec can't decode byte 0xcd in position 4: invalid continuation byte -->
```

### `.git/objects/48/8c6260c10f2e88fa1fae58a63fccec8d600cd1`
**(No description)**
```python
<!-- ERROR reading 8c6260c10f2e88fa1fae58a63fccec8d600cd1: 'utf-8' codec can't decode byte 0x9b in position 6: invalid start byte -->
```

### `.git/objects/48/d160d27a5d7276287b4c42f1a9037de8ac3e2f`
**(No description)**
```python
<!-- ERROR reading d160d27a5d7276287b4c42f1a9037de8ac3e2f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/48/f8ae06c19b4216c62893ccc78c222861f5a6ef`
**(No description)**
```python
<!-- ERROR reading f8ae06c19b4216c62893ccc78c222861f5a6ef: 'utf-8' codec can't decode byte 0xb4 in position 9: invalid start byte -->
```

### `.git/objects/48/fbc20e8c92c9140a72fb7a0d299e1e2b706452`
**(No description)**
```python
<!-- ERROR reading fbc20e8c92c9140a72fb7a0d299e1e2b706452: 'utf-8' codec can't decode byte 0xc8 in position 17: invalid continuation byte -->
```

### `.git/objects/70/369b9d663414c24f1e042c5b30a8f8c7bbd2b2`
**(No description)**
```python
<!-- ERROR reading 369b9d663414c24f1e042c5b30a8f8c7bbd2b2: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/70/4dfdffc8ba61eb913fa918072381e410b23c00`
**(No description)**
```python
<!-- ERROR reading 4dfdffc8ba61eb913fa918072381e410b23c00: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/70/88934c9bbb5f8591cf67424974345737be4c3d`
**(No description)**
```python
<!-- ERROR reading 88934c9bbb5f8591cf67424974345737be4c3d: 'utf-8' codec can't decode byte 0xcd in position 4: invalid continuation byte -->
```

### `.git/objects/70/a41cc7b490b084b5f84056df2b950fc02f3407`
**(No description)**
```python
<!-- ERROR reading a41cc7b490b084b5f84056df2b950fc02f3407: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/70/c2dca8a81fea5620185374ce22ba77c356027f`
**(No description)**
```python
<!-- ERROR reading c2dca8a81fea5620185374ce22ba77c356027f: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/70/ebd3d061b78da4e274dd81dec4492257044097`
**(No description)**
```python
<!-- ERROR reading ebd3d061b78da4e274dd81dec4492257044097: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/70/f0e059ed42bcca4ad99f4c2dfad14935f4cfea`
**(No description)**
```python
<!-- ERROR reading f0e059ed42bcca4ad99f4c2dfad14935f4cfea: 'utf-8' codec can't decode byte 0x99 in position 10: invalid start byte -->
```

### `.git/objects/1e/216a765d15d5dd9e379f9de4f8f91ab8063877`
**(No description)**
```python
<!-- ERROR reading 216a765d15d5dd9e379f9de4f8f91ab8063877: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/1e/313e1090ad02f984d96b11b1b47fc72301fb94`
**(No description)**
```python
<!-- ERROR reading 313e1090ad02f984d96b11b1b47fc72301fb94: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/1e/4b0bb8ddf072bc6e4b23794bf02b6e667ae800`
**(No description)**
```python
<!-- ERROR reading 4b0bb8ddf072bc6e4b23794bf02b6e667ae800: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/1e/ab7dd66d9bfdefea1a0e159303f1c09fa16d67`
**(No description)**
```python
<!-- ERROR reading ab7dd66d9bfdefea1a0e159303f1c09fa16d67: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/84/46d2dd959721cc86d4ae5a7699197454f3aa91`
**(No description)**
```python
<!-- ERROR reading 46d2dd959721cc86d4ae5a7699197454f3aa91: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/84/5bff4421f8700eb6e1bf719b0639185e6ed0b1`
**(No description)**
```python
<!-- ERROR reading 5bff4421f8700eb6e1bf719b0639185e6ed0b1: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/84/a402277054370fdbc8b25bc2e6d4501dbf9cbc`
**(No description)**
```python
<!-- ERROR reading a402277054370fdbc8b25bc2e6d4501dbf9cbc: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/84/df87a586adf44bb6135d547049b9f5385f30b7`
**(No description)**
```python
<!-- ERROR reading df87a586adf44bb6135d547049b9f5385f30b7: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/84/dfa4d0306a6a885004cbc5cc6f5a835fd46955`
**(No description)**
```python
<!-- ERROR reading dfa4d0306a6a885004cbc5cc6f5a835fd46955: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/84/e395fffe5ffdc56e5876fefc110501fc67ddb0`
**(No description)**
```python
<!-- ERROR reading e395fffe5ffdc56e5876fefc110501fc67ddb0: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/84/f798fc1a80413e57d3d2b6c8355e6c4a9dd10a`
**(No description)**
```python
<!-- ERROR reading f798fc1a80413e57d3d2b6c8355e6c4a9dd10a: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/4a/014283c8650112323007992fe702702707ad66`
**(No description)**
```python
<!-- ERROR reading 014283c8650112323007992fe702702707ad66: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/4a/389e4d071d3753f14a8b74338def21f6b54299`
**(No description)**
```python
<!-- ERROR reading 389e4d071d3753f14a8b74338def21f6b54299: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/4a/4bb5d8f8176ffab6cea5b32c44a4cc12055fef`
**(No description)**
```python
<!-- ERROR reading 4bb5d8f8176ffab6cea5b32c44a4cc12055fef: 'utf-8' codec can't decode byte 0xb7 in position 8: invalid start byte -->
```

### `.git/objects/4a/7d55d0e50cb8b892caa021695522e5ddd54a17`
**(No description)**
```python
<!-- ERROR reading 7d55d0e50cb8b892caa021695522e5ddd54a17: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/4a/865012c16237c3c4dd3404af7ed767b98d235a`
**(No description)**
```python
<!-- ERROR reading 865012c16237c3c4dd3404af7ed767b98d235a: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/4a/a58c6a61ca7ac05e399e40ae80e31032aeeb4e`
**(No description)**
```python
<!-- ERROR reading a58c6a61ca7ac05e399e40ae80e31032aeeb4e: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/4a/b14e48c92aff0766e51afd69a875cdba81712d`
**(No description)**
```python
<!-- ERROR reading b14e48c92aff0766e51afd69a875cdba81712d: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/4a/b3cf70dcae57597d30ea8861b4eae59610eaf9`
**(No description)**
```python
<!-- ERROR reading b3cf70dcae57597d30ea8861b4eae59610eaf9: 'utf-8' codec can't decode byte 0xb6 in position 8: invalid start byte -->
```

### `.git/objects/24/033acfed095376d55b3e499ab9a6f016f3b5cc`
**(No description)**
```python
<!-- ERROR reading 033acfed095376d55b3e499ab9a6f016f3b5cc: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/24/7e63fc86c48856a1ae3cefda59b3f458949ab4`
**(No description)**
```python
<!-- ERROR reading 7e63fc86c48856a1ae3cefda59b3f458949ab4: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/24/9bd058760e0cb176314edfcea19a6eb7c98e14`
**(No description)**
```python
<!-- ERROR reading 9bd058760e0cb176314edfcea19a6eb7c98e14: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/24/9f728c062e901e9455c2084f5a9b2098276159`
**(No description)**
```python
<!-- ERROR reading 9f728c062e901e9455c2084f5a9b2098276159: 'utf-8' codec can't decode byte 0x8d in position 3: invalid start byte -->
```

### `.git/objects/24/d6a5dd31fe33b03f90ed0f9ee465253686900c`
**(No description)**
```python
<!-- ERROR reading d6a5dd31fe33b03f90ed0f9ee465253686900c: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/24/dbc9fba250275af44170f4f03d786d5ad66fa6`
**(No description)**
```python
<!-- ERROR reading dbc9fba250275af44170f4f03d786d5ad66fa6: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/24/ec9834d9a51c4147bf3d530a49820b46038f51`
**(No description)**
```python
<!-- ERROR reading ec9834d9a51c4147bf3d530a49820b46038f51: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/24/fb0a7c81bc665844d5d307eee2d720079c039f`
**(No description)**
```python
<!-- ERROR reading fb0a7c81bc665844d5d307eee2d720079c039f: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/24/fe4b320489212ce109538f7169efae5ba761ba`
**(No description)**
```python
<!-- ERROR reading fe4b320489212ce109538f7169efae5ba761ba: 'utf-8' codec can't decode byte 0xaa in position 6: invalid start byte -->
```

### `.git/objects/23/0264591f0bb5fa38412acba37cf0bbaa649dad`
**(No description)**
```python
<!-- ERROR reading 0264591f0bb5fa38412acba37cf0bbaa649dad: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/23/1f81d11b87ef05d4765cd61d88d7348eb9e401`
**(No description)**
```python
<!-- ERROR reading 1f81d11b87ef05d4765cd61d88d7348eb9e401: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/23/450953df74eccd9c13cd2a955ce09d1f968565`
**(No description)**
```python
<!-- ERROR reading 450953df74eccd9c13cd2a955ce09d1f968565: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/23/886ff1581a16aa97e5c375e62261622e24c169`
**(No description)**
```python
<!-- ERROR reading 886ff1581a16aa97e5c375e62261622e24c169: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/4f/379fd2662e73d480c2bc538f38409245468668`
**(No description)**
```python
<!-- ERROR reading 379fd2662e73d480c2bc538f38409245468668: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/4f/80e28fc7102230107ec101abcbd68192d47725`
**(No description)**
```python
<!-- ERROR reading 80e28fc7102230107ec101abcbd68192d47725: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/4f/924a607895bebbfa308eb8797a8ace5ccc0dfb`
**(No description)**
```python
<!-- ERROR reading 924a607895bebbfa308eb8797a8ace5ccc0dfb: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/4f/d866412b5e32fc333866cfea8271f3a7116907`
**(No description)**
```python
<!-- ERROR reading d866412b5e32fc333866cfea8271f3a7116907: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/4f/fe870fee449aa915593d1559c56b0b3cc3db09`
**(No description)**
```python
<!-- ERROR reading fe870fee449aa915593d1559c56b0b3cc3db09: 'utf-8' codec can't decode byte 0xca in position 20: invalid continuation byte -->
```

### `.git/objects/8d/1e2a81c5f0d1bd858bf12ccf15b1461008cf99`
**(No description)**
```python
<!-- ERROR reading 1e2a81c5f0d1bd858bf12ccf15b1461008cf99: 'utf-8' codec can't decode byte 0x8b in position 3: invalid start byte -->
```

### `.git/objects/8d/3301e9daf73b474162d712f4b87f54ccd97a16`
**(No description)**
```python
<!-- ERROR reading 3301e9daf73b474162d712f4b87f54ccd97a16: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/8d/faad0dbb3ff5300cccb2023748cd30f54bc920`
**(No description)**
```python
<!-- ERROR reading faad0dbb3ff5300cccb2023748cd30f54bc920: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/15/04a12916b10c2de007d0ac0e1a3531ac79f8a7`
**(No description)**
```python
<!-- ERROR reading 04a12916b10c2de007d0ac0e1a3531ac79f8a7: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte -->
```

### `.git/objects/15/29287401e51dd26768f95048c1f6e57430ad77`
**(No description)**
```python
<!-- ERROR reading 29287401e51dd26768f95048c1f6e57430ad77: 'utf-8' codec can't decode byte 0xb7 in position 9: invalid start byte -->
```

### `.git/objects/15/42de02d2b6851f2b901152d8eda0db0cd144f0`
**(No description)**
```python
<!-- ERROR reading 42de02d2b6851f2b901152d8eda0db0cd144f0: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/15/77dad7db498d232e9305cb1518da9cec902e30`
**(No description)**
```python
<!-- ERROR reading 77dad7db498d232e9305cb1518da9cec902e30: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/12/228d414b6cfed7c39d3781c85c63256a1d7fb5`
**(No description)**
```python
<!-- ERROR reading 228d414b6cfed7c39d3781c85c63256a1d7fb5: 'utf-8' codec can't decode byte 0xc9 in position 3: invalid continuation byte -->
```

### `.git/objects/12/619d69a83b7d1f6825944f8cbaf40467a459c0`
**(No description)**
```python
<!-- ERROR reading 619d69a83b7d1f6825944f8cbaf40467a459c0: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte -->
```

### `.git/objects/12/650804ae0331efea9f053b956c47cca3946e08`
**(No description)**
```python
<!-- ERROR reading 650804ae0331efea9f053b956c47cca3946e08: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/12/c79b49a2a52bdff96ef7849f6b7aed59f6ed23`
**(No description)**
```python
<!-- ERROR reading c79b49a2a52bdff96ef7849f6b7aed59f6ed23: 'utf-8' codec can't decode byte 0x90 in position 3: invalid start byte -->
```

### `.git/objects/12/fef106e53a8e7147b18cb2bb2545de7f646a00`
**(No description)**
```python
<!-- ERROR reading fef106e53a8e7147b18cb2bb2545de7f646a00: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/8c/167ffcb4497f1cee666f3797804e08278b5c2a`
**(No description)**
```python
<!-- ERROR reading 167ffcb4497f1cee666f3797804e08278b5c2a: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/8c/1d9e5f605a4b8dd3809b556f876087bd63d242`
**(No description)**
```python
<!-- ERROR reading 1d9e5f605a4b8dd3809b556f876087bd63d242: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/8c/418f59e06cae43abdbb626ec21cafc7e8c6277`
**(No description)**
```python
<!-- ERROR reading 418f59e06cae43abdbb626ec21cafc7e8c6277: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/8c/4dc9a8b0005328b061727a21c52fe2ea8e46d0`
**(No description)**
```python
<!-- ERROR reading 4dc9a8b0005328b061727a21c52fe2ea8e46d0: 'utf-8' codec can't decode byte 0xc4 in position 6: invalid continuation byte -->
```

### `.git/objects/8c/8148c2a17371e796d895543acbae8841c6a970`
**(No description)**
```python
<!-- ERROR reading 8148c2a17371e796d895543acbae8841c6a970: 'utf-8' codec can't decode byte 0x85 in position 14: invalid start byte -->
```

### `.git/objects/8c/ecd4f93398819912b35309d5ad44f61a3f7270`
**(No description)**
```python
<!-- ERROR reading ecd4f93398819912b35309d5ad44f61a3f7270: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/85/1dce9d381d7b952bca3223e073b35eb694f0df`
**(No description)**
```python
<!-- ERROR reading 1dce9d381d7b952bca3223e073b35eb694f0df: 'utf-8' codec can't decode byte 0x8b in position 5: invalid start byte -->
```

### `.git/objects/85/450fafa34733d81dd8d5c52637a464e5399efa`
**(No description)**
```python
<!-- ERROR reading 450fafa34733d81dd8d5c52637a464e5399efa: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/85/55ee0780e98b052eb463d55a1c18e39b257762`
**(No description)**
```python
<!-- ERROR reading 55ee0780e98b052eb463d55a1c18e39b257762: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/85/92ffe017a87367cc7578184540096a9682908d`
**(No description)**
```python
<!-- ERROR reading 92ffe017a87367cc7578184540096a9682908d: 'utf-8' codec can't decode bytes in position 6-7: invalid continuation byte -->
```

### `.git/objects/85/aa46327023e1f83537199647d4f85359398703`
**(No description)**
```python
<!-- ERROR reading aa46327023e1f83537199647d4f85359398703: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/85/b4905cbc292618ce8e50e9318791b584ba6026`
**(No description)**
```python
<!-- ERROR reading b4905cbc292618ce8e50e9318791b584ba6026: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/85/f4dd63d2da8e31d7e84d5180f016fdfe315c2c`
**(No description)**
```python
<!-- ERROR reading f4dd63d2da8e31d7e84d5180f016fdfe315c2c: 'utf-8' codec can't decode byte 0x8f in position 5: invalid start byte -->
```

### `.git/objects/1d/16ab769c88f28febd7b65f93693663a492e264`
**(No description)**
```python
<!-- ERROR reading 16ab769c88f28febd7b65f93693663a492e264: 'utf-8' codec can't decode byte 0xb5 in position 9: invalid start byte -->
```

### `.git/objects/1d/23ee5fe24a217ffea0d0e424d20d7732618fd4`
**(No description)**
```python
<!-- ERROR reading 23ee5fe24a217ffea0d0e424d20d7732618fd4: 'utf-8' codec can't decode byte 0xd0 in position 19: invalid continuation byte -->
```

### `.git/objects/1d/49897fe860a4d081fe6a70434bebb1238b7f52`
**(No description)**
```python
<!-- ERROR reading 49897fe860a4d081fe6a70434bebb1238b7f52: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/1d/5314b706c8b673544d2254831d95748e9b7e3c`
**(No description)**
```python
<!-- ERROR reading 5314b706c8b673544d2254831d95748e9b7e3c: 'utf-8' codec can't decode byte 0xef in position 4: invalid continuation byte -->
```

### `.git/objects/1d/727e9b3461b308dbb627c1b0fbecf8d9538e29`
**(No description)**
```python
<!-- ERROR reading 727e9b3461b308dbb627c1b0fbecf8d9538e29: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/1d/e32cfb6191abd5f5f74f4154f83e08d050a870`
**(No description)**
```python
<!-- ERROR reading e32cfb6191abd5f5f74f4154f83e08d050a870: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/1d/f9f2a70e6815908f2784e88897a9a359eef84c`
**(No description)**
```python
<!-- ERROR reading f9f2a70e6815908f2784e88897a9a359eef84c: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/71/0e03e4fe0e37ea1bbd3fbbc09933db4e120f4a`
**(No description)**
```python
<!-- ERROR reading 0e03e4fe0e37ea1bbd3fbbc09933db4e120f4a: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/71/62e25d50aac2712e9919352871b3779e58f546`
**(No description)**
```python
<!-- ERROR reading 62e25d50aac2712e9919352871b3779e58f546: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/71/6ca403ae0894726d21408ca83913219fc92500`
**(No description)**
```python
<!-- ERROR reading 6ca403ae0894726d21408ca83913219fc92500: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/71/9be04033fbb9c38bb5b6a883c396563c54f4c2`
**(No description)**
```python
<!-- ERROR reading 9be04033fbb9c38bb5b6a883c396563c54f4c2: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/71/f17c506aa92412820ca41d09c17894034e6f17`
**(No description)**
```python
<!-- ERROR reading f17c506aa92412820ca41d09c17894034e6f17: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/71/f4a94a4fa44a6f9423dc6c5305f928fd72b9e0`
**(No description)**
```python
<!-- ERROR reading f4a94a4fa44a6f9423dc6c5305f928fd72b9e0: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/76/32ecf77545c5e5501cb3fc5719df0761104ca2`
**(No description)**
```python
<!-- ERROR reading 32ecf77545c5e5501cb3fc5719df0761104ca2: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/76/341dd863c79e1562d64c998ef42008b3f5964f`
**(No description)**
```python
<!-- ERROR reading 341dd863c79e1562d64c998ef42008b3f5964f: 'utf-8' codec can't decode byte 0xc4 in position 6: invalid continuation byte -->
```

### `.git/objects/76/47fd0f0f50f93c2a5e97c2fdf06398ae7d7786`
**(No description)**
```python
<!-- ERROR reading 47fd0f0f50f93c2a5e97c2fdf06398ae7d7786: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/76/a260e5083120032507e992d80d26a9b14099d0`
**(No description)**
```python
<!-- ERROR reading a260e5083120032507e992d80d26a9b14099d0: 'utf-8' codec can't decode byte 0xf0 in position 17: invalid continuation byte -->
```

### `.git/objects/76/ad776be2272b6ee6ad1e5cd948762465bf0dcc`
**(No description)**
```python
<!-- ERROR reading ad776be2272b6ee6ad1e5cd948762465bf0dcc: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/76/ddb334834425d77d231f3bb91346c2dbe1d000`
**(No description)**
```python
<!-- ERROR reading ddb334834425d77d231f3bb91346c2dbe1d000: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/76/f47ffd08949652131d159888096151ef223f14`
**(No description)**
```python
<!-- ERROR reading f47ffd08949652131d159888096151ef223f14: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/1c/06844de5f1e1fa06394e42d11259c65555cd14`
**(No description)**
```python
<!-- ERROR reading 06844de5f1e1fa06394e42d11259c65555cd14: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/1c/5677012173b63a1af3d02be818e0aacd507a80`
**(No description)**
```python
<!-- ERROR reading 5677012173b63a1af3d02be818e0aacd507a80: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/1c/6a450cdcd1e66ed55685438e8f6f393ccfa828`
**(No description)**
```python
<!-- ERROR reading 6a450cdcd1e66ed55685438e8f6f393ccfa828: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/1c/73f6c9a5d4c30a16f2b6ca875e0c75ece1dfc1`
**(No description)**
```python
<!-- ERROR reading 73f6c9a5d4c30a16f2b6ca875e0c75ece1dfc1: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/1c/826835b495b15c44810f1f6b8ff4d3b2833f74`
**(No description)**
```python
<!-- ERROR reading 826835b495b15c44810f1f6b8ff4d3b2833f74: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/1c/83c8ed3d618cd68e774a30be6737da1dda8b15`
**(No description)**
```python
<!-- ERROR reading 83c8ed3d618cd68e774a30be6737da1dda8b15: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/1c/9ff35446d864fc8dd06b02754b9277b7f65705`
**(No description)**
```python
<!-- ERROR reading 9ff35446d864fc8dd06b02754b9277b7f65705: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/1c/cc8752507ba337c39d9252038a0ceb1df25e0e`
**(No description)**
```python
<!-- ERROR reading cc8752507ba337c39d9252038a0ceb1df25e0e: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/1c/d8e07279ae7b5e11954d5aaf7d3be03d107cb6`
**(No description)**
```python
<!-- ERROR reading d8e07279ae7b5e11954d5aaf7d3be03d107cb6: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/1c/f68185e6d5b5fbbaae6c66b2d641c1a0bb45d3`
**(No description)**
```python
<!-- ERROR reading f68185e6d5b5fbbaae6c66b2d641c1a0bb45d3: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/82/13f062051981459b641a65f2eef0568efd9b56`
**(No description)**
```python
<!-- ERROR reading 13f062051981459b641a65f2eef0568efd9b56: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/82/24f089d6e0afd45dc0893125e92d25483d09d5`
**(No description)**
```python
<!-- ERROR reading 24f089d6e0afd45dc0893125e92d25483d09d5: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/82/42644b8e39d498d92c217e96a6370910efacd0`
**(No description)**
```python
<!-- ERROR reading 42644b8e39d498d92c217e96a6370910efacd0: 'utf-8' codec can't decode byte 0xd5 in position 26: invalid continuation byte -->
```

### `.git/objects/82/8889f49e6a6e235c1a73d365a1459754c14160`
**(No description)**
```python
<!-- ERROR reading 8889f49e6a6e235c1a73d365a1459754c14160: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/82/8afe512b178d8625c3cef2a6c1c24b0aeb1072`
**(No description)**
```python
<!-- ERROR reading 8afe512b178d8625c3cef2a6c1c24b0aeb1072: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/82/a47cdae8b3fa48189f578e5e49e67f4f4ae443`
**(No description)**
```python
<!-- ERROR reading a47cdae8b3fa48189f578e5e49e67f4f4ae443: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/82/a77384dcbc56690494ad4549ef859071d90af2`
**(No description)**
```python
<!-- ERROR reading a77384dcbc56690494ad4549ef859071d90af2: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/82/faa632195560021e6902dea036c9198c0713e9`
**(No description)**
```python
<!-- ERROR reading faa632195560021e6902dea036c9198c0713e9: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte -->
```

### `.git/objects/49/0e4fb13d24df22eafb9b5164d20a11b017da08`
**(No description)**
```python
<!-- ERROR reading 0e4fb13d24df22eafb9b5164d20a11b017da08: 'utf-8' codec can't decode byte 0xc8 in position 18: invalid continuation byte -->
```

### `.git/objects/49/2c2c70584dc3421f81dded94972c236737cefd`
**(No description)**
```python
<!-- ERROR reading 2c2c70584dc3421f81dded94972c236737cefd: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/49/3b53e4e7a3984ddd49780313bf3bd9901dc1e0`
**(No description)**
```python
<!-- ERROR reading 3b53e4e7a3984ddd49780313bf3bd9901dc1e0: 'utf-8' codec can't decode byte 0x8e in position 3: invalid start byte -->
```

### `.git/objects/49/4f34204fc004f2be964bd227cb0c7a303d8351`
**(No description)**
```python
<!-- ERROR reading 4f34204fc004f2be964bd227cb0c7a303d8351: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/49/5de2ae7111ef3b0382f5efe11a0e8e7cbd186b`
**(No description)**
```python
<!-- ERROR reading 5de2ae7111ef3b0382f5efe11a0e8e7cbd186b: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/49/6a45428e3b64e3b7b9689c96e574ff8ce099f1`
**(No description)**
```python
<!-- ERROR reading 6a45428e3b64e3b7b9689c96e574ff8ce099f1: 'utf-8' codec can't decode byte 0xd6 in position 22: invalid continuation byte -->
```

### `.git/objects/49/c671a7fab852ccac97cda28084066e3bc5f97e`
**(No description)**
```python
<!-- ERROR reading c671a7fab852ccac97cda28084066e3bc5f97e: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/49/dd6a0bbbb60af5cdd2c8e48dc08ed3ac5d8784`
**(No description)**
```python
<!-- ERROR reading dd6a0bbbb60af5cdd2c8e48dc08ed3ac5d8784: 'utf-8' codec can't decode bytes in position 2-3: invalid continuation byte -->
```

### `.git/objects/49/f0e698c97ad5623f376d8182675352e21c2c3c`
**(No description)**
```python
<!-- ERROR reading f0e698c97ad5623f376d8182675352e21c2c3c: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/40/0fb45dd0869f3c173a2e16a99894a15c484c18`
**(No description)**
```python
<!-- ERROR reading 0fb45dd0869f3c173a2e16a99894a15c484c18: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/40/12406aa76f743c5c5d1ab8ff56d6d67cfb6653`
**(No description)**
```python
<!-- ERROR reading 12406aa76f743c5c5d1ab8ff56d6d67cfb6653: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/40/18a09c6fb1e0ef1b03ab8d84b13ebef4031f7c`
**(No description)**
```python
<!-- ERROR reading 18a09c6fb1e0ef1b03ab8d84b13ebef4031f7c: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/40/4986db114e718488e9ec4a619f2dad0909cfb3`
**(No description)**
```python
<!-- ERROR reading 4986db114e718488e9ec4a619f2dad0909cfb3: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/40/5de593f237c4f8114406bc73618233d7bbabb9`
**(No description)**
```python
<!-- ERROR reading 5de593f237c4f8114406bc73618233d7bbabb9: 'utf-8' codec can't decode byte 0xc9 in position 4: invalid continuation byte -->
```

### `.git/objects/2e/18f1bac7f3d8028c2aea94346baf78f732225a`
**(No description)**
```python
<!-- ERROR reading 18f1bac7f3d8028c2aea94346baf78f732225a: 'utf-8' codec can't decode byte 0x88 in position 18: invalid start byte -->
```

### `.git/objects/2e/9d8757a582b1dcdb47a34c35c6cfb3ed23ba90`
**(No description)**
```python
<!-- ERROR reading 9d8757a582b1dcdb47a34c35c6cfb3ed23ba90: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/2e/be3476633e2850f4b09041291864fb14b717d8`
**(No description)**
```python
<!-- ERROR reading be3476633e2850f4b09041291864fb14b717d8: 'utf-8' codec can't decode byte 0xcf in position 4: invalid continuation byte -->
```

### `.git/objects/2e/c79e65bea5df7f379451a50b7cc9fe6ce0832f`
**(No description)**
```python
<!-- ERROR reading c79e65bea5df7f379451a50b7cc9fe6ce0832f: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/2e/cc9e9c363e2f16c4f934cf41cf871826d6a495`
**(No description)**
```python
<!-- ERROR reading cc9e9c363e2f16c4f934cf41cf871826d6a495: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/2e/ed4ef8fc5fdbe738297ca030d8774dd2e1cb10`
**(No description)**
```python
<!-- ERROR reading ed4ef8fc5fdbe738297ca030d8774dd2e1cb10: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/2b/08d6e741929871cdece4489a3a9019921ab37a`
**(No description)**
```python
<!-- ERROR reading 08d6e741929871cdece4489a3a9019921ab37a: 'utf-8' codec can't decode byte 0x8f in position 3: invalid start byte -->
```

### `.git/objects/2b/45d391d4d7398e4769f45f9dd25eb55daef437`
**(No description)**
```python
<!-- ERROR reading 45d391d4d7398e4769f45f9dd25eb55daef437: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/2b/47c0eac92162646c8b60bd3de65bff1951c895`
**(No description)**
```python
<!-- ERROR reading 47c0eac92162646c8b60bd3de65bff1951c895: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/2b/7b7fb88c0b204e929dbec3ad59016aa381b2af`
**(No description)**
```python
<!-- ERROR reading 7b7fb88c0b204e929dbec3ad59016aa381b2af: 'utf-8' codec can't decode byte 0xef in position 4: invalid continuation byte -->
```

### `.git/objects/2b/a6f9b8bcc8ecb71555fce33d236d94463185ee`
**(No description)**
```python
<!-- ERROR reading a6f9b8bcc8ecb71555fce33d236d94463185ee: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/2b/c4efae0e1b14620f75f712eb15ecf500d14eef`
**(No description)**
```python
<!-- ERROR reading c4efae0e1b14620f75f712eb15ecf500d14eef: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/47/065fb58860e9b1de1f1177e5ae803a20908073`
**(No description)**
```python
<!-- ERROR reading 065fb58860e9b1de1f1177e5ae803a20908073: 'utf-8' codec can't decode byte 0xf0 in position 18: invalid continuation byte -->
```

### `.git/objects/47/20170012386e15ee962e39c9d8272809da5eb8`
**(No description)**
```python
<!-- ERROR reading 20170012386e15ee962e39c9d8272809da5eb8: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/47/40c467553614cde9c27a1f4bb74f42c8ee0165`
**(No description)**
```python
<!-- ERROR reading 40c467553614cde9c27a1f4bb74f42c8ee0165: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/47/60c1ffc42137ed3ba4735b5080f6cb87846bee`
**(No description)**
```python
<!-- ERROR reading 60c1ffc42137ed3ba4735b5080f6cb87846bee: 'utf-8' codec can't decode byte 0xcc in position 3: invalid continuation byte -->
```

### `.git/objects/47/7cbe6b1aafd69f86096ecc8d633950df0fd5ac`
**(No description)**
```python
<!-- ERROR reading 7cbe6b1aafd69f86096ecc8d633950df0fd5ac: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte -->
```

### `.git/objects/47/af547d6fcc6a947d7bde12be92daeb08075722`
**(No description)**
```python
<!-- ERROR reading af547d6fcc6a947d7bde12be92daeb08075722: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/47/efd792b3cd04f0646adf7d3ef1811d201f8873`
**(No description)**
```python
<!-- ERROR reading efd792b3cd04f0646adf7d3ef1811d201f8873: 'utf-8' codec can't decode byte 0xbd in position 2: invalid start byte -->
```

### `.git/objects/78/1dfa2d7c489d3a5ec207a63522e771d3cef22a`
**(No description)**
```python
<!-- ERROR reading 1dfa2d7c489d3a5ec207a63522e771d3cef22a: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/78/24d326e71f14c931dab083b56e942fef5ad963`
**(No description)**
```python
<!-- ERROR reading 24d326e71f14c931dab083b56e942fef5ad963: 'utf-8' codec can't decode byte 0xdb in position 6: invalid continuation byte -->
```

### `.git/objects/78/55226e4b500142deef8fb247cd33a9a991d122`
**(No description)**
```python
<!-- ERROR reading 55226e4b500142deef8fb247cd33a9a991d122: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/78/c52f17aa992f491d7f12a0b69d4c3a8d11338d`
**(No description)**
```python
<!-- ERROR reading c52f17aa992f491d7f12a0b69d4c3a8d11338d: 'utf-8' codec can't decode byte 0xb7 in position 8: invalid start byte -->
```

### `.git/objects/8b/137891791fe96927ad78e64b0aad7bded08bdc`
**(No description)**
```python
<!-- ERROR reading 137891791fe96927ad78e64b0aad7bded08bdc: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/8b/3ff014edce1fb5974ee70ebb23aa6460f62bf7`
**(No description)**
```python
<!-- ERROR reading 3ff014edce1fb5974ee70ebb23aa6460f62bf7: 'utf-8' codec can't decode byte 0xc5 in position 2: invalid continuation byte -->
```

### `.git/objects/8b/93059e19faa9f821ffad1b8a298e7301fe8ab2`
**(No description)**
```python
<!-- ERROR reading 93059e19faa9f821ffad1b8a298e7301fe8ab2: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/8b/e6928a31feca4549a6ec789a8db751d5bb8c97`
**(No description)**
```python
<!-- ERROR reading e6928a31feca4549a6ec789a8db751d5bb8c97: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/13/3a6231a5b53fd2f073799ca1bd07c50abe40ae`
**(No description)**
```python
<!-- ERROR reading 3a6231a5b53fd2f073799ca1bd07c50abe40ae: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/13/e50b1ef9e9a1dbe81c4514cd7c7ba8909a4a38`
**(No description)**
```python
<!-- ERROR reading e50b1ef9e9a1dbe81c4514cd7c7ba8909a4a38: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/7f/258c57481df7b36988f8bb790b79ea402a71de`
**(No description)**
```python
<!-- ERROR reading 258c57481df7b36988f8bb790b79ea402a71de: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/7f/5613e88e554b514ca09aa6b81cd8d164bfecb7`
**(No description)**
```python
<!-- ERROR reading 5613e88e554b514ca09aa6b81cd8d164bfecb7: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/7f/62d5da3c7a3b2259f44a6f8ca752b0830e76ad`
**(No description)**
```python
<!-- ERROR reading 62d5da3c7a3b2259f44a6f8ca752b0830e76ad: 'utf-8' codec can't decode byte 0xa2 in position 6: invalid start byte -->
```

### `.git/objects/7f/e827da4d071b32ea6da44328629699d6fc88ce`
**(No description)**
```python
<!-- ERROR reading e827da4d071b32ea6da44328629699d6fc88ce: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/7f/ff2ac3355cb6bdaf39919518c3c481e6724336`
**(No description)**
```python
<!-- ERROR reading ff2ac3355cb6bdaf39919518c3c481e6724336: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/7a/073cf69291e99faef1f9a7152f569487a89e52`
**(No description)**
```python
<!-- ERROR reading 073cf69291e99faef1f9a7152f569487a89e52: 'utf-8' codec can't decode byte 0xc9 in position 21: invalid continuation byte -->
```

### `.git/objects/7a/17b7b3b6ad49157ee41f3da304fec3d32342d3`
**(No description)**
```python
<!-- ERROR reading 17b7b3b6ad49157ee41f3da304fec3d32342d3: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/7a/20ba1e46fcca03035f646e3a7f3dc006c6bcd7`
**(No description)**
```python
<!-- ERROR reading 20ba1e46fcca03035f646e3a7f3dc006c6bcd7: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/7a/321053b29bcd48698cf2bd74a1d19c8556aefb`
**(No description)**
```python
<!-- ERROR reading 321053b29bcd48698cf2bd74a1d19c8556aefb: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/7a/51f212c8a08fc6a04e509e89d8dcc85185df77`
**(No description)**
```python
<!-- ERROR reading 51f212c8a08fc6a04e509e89d8dcc85185df77: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte -->
```

### `.git/objects/7a/52793faf9357c95a8b6861daf429113267a05e`
**(No description)**
```python
<!-- ERROR reading 52793faf9357c95a8b6861daf429113267a05e: 'utf-8' codec can't decode byte 0xb1 in position 8: invalid start byte -->
```

### `.git/objects/7a/b696c18cdc7c133ebc2d1b22d35c00f1a2ef55`
**(No description)**
```python
<!-- ERROR reading b696c18cdc7c133ebc2d1b22d35c00f1a2ef55: 'utf-8' codec can't decode byte 0xb2 in position 8: invalid start byte -->
```

### `.git/objects/7a/e8eeaa798960cd9fc18f0a259ec227fabf0ba7`
**(No description)**
```python
<!-- ERROR reading e8eeaa798960cd9fc18f0a259ec227fabf0ba7: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/7a/f58a0c9e500e268854dbe37795059cba78f52f`
**(No description)**
```python
<!-- ERROR reading f58a0c9e500e268854dbe37795059cba78f52f: 'utf-8' codec can't decode byte 0xb3 in position 8: invalid start byte -->
```

### `.git/objects/14/052d87af6e752e13de8dbdcfb42b44487cb407`
**(No description)**
```python
<!-- ERROR reading 052d87af6e752e13de8dbdcfb42b44487cb407: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte -->
```

### `.git/objects/14/213b307b96d6bbe0b39042f8feb2ac9a6e0b06`
**(No description)**
```python
<!-- ERROR reading 213b307b96d6bbe0b39042f8feb2ac9a6e0b06: 'utf-8' codec can't decode byte 0xb0 in position 7: invalid start byte -->
```

### `.git/objects/14/440a10dde4c302a4e75f831a376554dfd15177`
**(No description)**
```python
<!-- ERROR reading 440a10dde4c302a4e75f831a376554dfd15177: 'utf-8' codec can't decode byte 0xcd in position 4: invalid continuation byte -->
```

### `.git/objects/14/77117e26e4004ad800880ccee4bd052736b8c1`
**(No description)**
```python
<!-- ERROR reading 77117e26e4004ad800880ccee4bd052736b8c1: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/14/79c8694bfbd583a896dbe9bd33cdb6d7e7371e`
**(No description)**
```python
<!-- ERROR reading 79c8694bfbd583a896dbe9bd33cdb6d7e7371e: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/14/7a8fa333acaf31618d37ba2896e3a5bf5e4d02`
**(No description)**
```python
<!-- ERROR reading 7a8fa333acaf31618d37ba2896e3a5bf5e4d02: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/14/876000de895a609d5b9f3de39c3c8fc44ef1fc`
**(No description)**
```python
<!-- ERROR reading 876000de895a609d5b9f3de39c3c8fc44ef1fc: 'utf-8' codec can't decode byte 0xcd in position 2: invalid continuation byte -->
```

### `.git/objects/14/c7668cb3fc50d71a79b1af1d29b7dc18742660`
**(No description)**
```python
<!-- ERROR reading c7668cb3fc50d71a79b1af1d29b7dc18742660: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/objects/14/d745eefbb4c0c959c6f856a8147047578851cd`
**(No description)**
```python
<!-- ERROR reading d745eefbb4c0c959c6f856a8147047578851cd: 'utf-8' codec can't decode byte 0xe5 in position 2: invalid continuation byte -->
```

### `.git/objects/8e/2111a52ba7d5dc2a361d03303d93261c25abd5`
**(No description)**
```python
<!-- ERROR reading 2111a52ba7d5dc2a361d03303d93261c25abd5: 'utf-8' codec can't decode byte 0xdd in position 2: invalid continuation byte -->
```

### `.git/objects/8e/86594c5b94d8d13617e2816779c76c9560e57c`
**(No description)**
```python
<!-- ERROR reading 86594c5b94d8d13617e2816779c76c9560e57c: 'utf-8' codec can't decode byte 0xb6 in position 9: invalid start byte -->
```

### `.git/objects/8e/94b38f70f18871ebb7212342d02a75a939cd8e`
**(No description)**
```python
<!-- ERROR reading 94b38f70f18871ebb7212342d02a75a939cd8e: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte -->
```

### `.git/objects/8e/b8ec9605c73aeba33b5a2031d59a84d6841225`
**(No description)**
```python
<!-- ERROR reading b8ec9605c73aeba33b5a2031d59a84d6841225: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/8e/badae4f823189158dce696aded16c5072c14e2`
**(No description)**
```python
<!-- ERROR reading badae4f823189158dce696aded16c5072c14e2: 'utf-8' codec can't decode byte 0xd5 in position 2: invalid continuation byte -->
```

### `.git/objects/8e/e0ba7a082a04bfb91a6e1c7d80c5d51c0a2573`
**(No description)**
```python
<!-- ERROR reading e0ba7a082a04bfb91a6e1c7d80c5d51c0a2573: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte -->
```

### `.git/objects/8e/f6b28ea2ec097ae6ab5d9ac9b2e0d3fc8f4809`
**(No description)**
```python
<!-- ERROR reading f6b28ea2ec097ae6ab5d9ac9b2e0d3fc8f4809: 'utf-8' codec can't decode byte 0x8d in position 2: invalid start byte -->
```

### `.git/objects/22/2157873da628cee3046709dfd3a5825a30769b`
**(No description)**
```python
<!-- ERROR reading 2157873da628cee3046709dfd3a5825a30769b: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/22/49231f8c3b912c731ff160344d3672e2f11738`
**(No description)**
```python
<!-- ERROR reading 49231f8c3b912c731ff160344d3672e2f11738: 'utf-8' codec can't decode byte 0xed in position 2: invalid continuation byte -->
```

### `.git/objects/22/85457bf181d31d36b74ba6c368eac604178645`
**(No description)**
```python
<!-- ERROR reading 85457bf181d31d36b74ba6c368eac604178645: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte -->
```

### `.git/objects/25/103383ec7abc7b46fb6a6f549efa38e4abe24c`
**(No description)**
```python
<!-- ERROR reading 103383ec7abc7b46fb6a6f549efa38e4abe24c: 'utf-8' codec can't decode byte 0xa5 in position 2: invalid start byte -->
```

### `.git/objects/25/f4282cc29cb03d7be881f03dee841d7dbc215a`
**(No description)**
```python
<!-- ERROR reading f4282cc29cb03d7be881f03dee841d7dbc215a: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte -->
```

### `.git/info/exclude`
**git ls-files --others --exclude-from=.git/info/exclude**
```python
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~

```

### `.git/logs/HEAD`
**(No description)**
```python
0000000000000000000000000000000000000000 b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 Steven <steven.cohen714@gmail.com> 1743911110 +0200	commit (initial): Initial commit: Universal Recycling project
b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 0000000000000000000000000000000000000000 Steven <steven.cohen714@gmail.com> 1743911697 +0200	Branch: renamed refs/heads/master to refs/heads/main
0000000000000000000000000000000000000000 b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 Steven <steven.cohen714@gmail.com> 1743911697 +0200	Branch: renamed refs/heads/master to refs/heads/main
b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 463dd88259cdc9a8a289f03e930db5e3ca01c059 Steven <steven.cohen714@gmail.com> 1743913278 +0200	commit (merge): Fix README merge conflict
463dd88259cdc9a8a289f03e930db5e3ca01c059 a22748f497f0a30fbfe7468c21e519a2887d295a Steven <steven.cohen714@gmail.com> 1743918421 +0200	commit: Fixed status capitalization in backend and frontend
a22748f497f0a30fbfe7468c21e519a2887d295a 4720170012386e15ee962e39c9d8272809da5eb8 Steven <steven.cohen714@gmail.com> 1743921810 +0200	commit: Updated files
4720170012386e15ee962e39c9d8272809da5eb8 7d4bf87e7208b0b536d5f4879bbcf4bace79763f Steven <steven.cohen714@gmail.com> 1744516215 +0200	reset: moving to origin/main
7d4bf87e7208b0b536d5f4879bbcf4bace79763f 0934f4eaf144035330f565464b89411da235a172 Steven <steven.cohen714@gmail.com> 1744518214 +0200	commit: Add GET /orders endpoint
0934f4eaf144035330f565464b89411da235a172 0934f4eaf144035330f565464b89411da235a172 Steven <steven.cohen714@gmail.com> 1744525319 +0200	reset: moving to HEAD
0934f4eaf144035330f565464b89411da235a172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744525376 +0200	pull origin main: Fast-forward
b82c89c5571c7707f3d426c928ea247e8c2d7172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744528698 +0200	reset: moving to HEAD
b82c89c5571c7707f3d426c928ea247e8c2d7172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744529137 +0200	reset: moving to HEAD
b82c89c5571c7707f3d426c928ea247e8c2d7172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744529439 +0200	reset: moving to HEAD
b82c89c5571c7707f3d426c928ea247e8c2d7172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744530168 +0200	reset: moving to origin/main
b82c89c5571c7707f3d426c928ea247e8c2d7172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744530275 +0200	reset: moving to origin/main
b82c89c5571c7707f3d426c928ea247e8c2d7172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744530365 +0200	reset: moving to origin/main
b82c89c5571c7707f3d426c928ea247e8c2d7172 e28f74abef4ca5048cf1503f9a130554cf5970cf Steven <steven.cohen714@gmail.com> 1744530464 +0200	commit: Force sync scripts with correct names
e28f74abef4ca5048cf1503f9a130554cf5970cf e28f74abef4ca5048cf1503f9a130554cf5970cf Steven <steven.cohen714@gmail.com> 1744860712 +0200	reset: moving to HEAD
e28f74abef4ca5048cf1503f9a130554cf5970cf 075eefe5307e9389ac202171d47ec626b84cb35c Steven <steven.cohen714@gmail.com> 1744860719 +0200	pull --rebase origin main: Fast-forward
075eefe5307e9389ac202171d47ec626b84cb35c 075eefe5307e9389ac202171d47ec626b84cb35c Steven <steven.cohen714@gmail.com> 1744860979 +0200	reset: moving to origin/main
075eefe5307e9389ac202171d47ec626b84cb35c a9adb8b6c85412eff2a43197f748b6d5dd9a8b6e Steven <steven.cohen714@gmail.com> 1744861041 +0200	commit: Resolved conflict in .DS_Store
a9adb8b6c85412eff2a43197f748b6d5dd9a8b6e 20d2770b6fecabeec22c38c28a289a18498ca7cd Steven <steven.cohen714@gmail.com> 1744861100 +0200	commit: Removed conflict junk in backend/endpoints/.DS_Store
20d2770b6fecabeec22c38c28a289a18498ca7cd 20d2770b6fecabeec22c38c28a289a18498ca7cd Steven <steven.cohen714@gmail.com> 1744862935 +0200	reset: moving to HEAD
20d2770b6fecabeec22c38c28a289a18498ca7cd 20d2770b6fecabeec22c38c28a289a18498ca7cd Steven <steven.cohen714@gmail.com> 1744863623 +0200	reset: moving to HEAD
20d2770b6fecabeec22c38c28a289a18498ca7cd 19b0d9fa6dbcbe8f9b08a709419372c8f445bc23 Steven <steven.cohen714@gmail.com> 1744899375 +0200	commit: Auto-commit for push (script)
19b0d9fa6dbcbe8f9b08a709419372c8f445bc23 acf94ac32d9a9d8e79d6ad1154d32675229ce6e0 Steven <steven.cohen714@gmail.com> 1744908994 +0200	commit: Auto-commit for push (script)
acf94ac32d9a9d8e79d6ad1154d32675229ce6e0 5dd1ab6da18ef67ae45007b5ace3440264dd0d5a Steven <steven.cohen714@gmail.com> 1744970528 +0200	commit: Auto-commit for push (script)
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a 5dd1ab6da18ef67ae45007b5ace3440264dd0d5a Steven <steven.cohen714@gmail.com> 1745039269 +0200	reset: moving to HEAD
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a 5dd1ab6da18ef67ae45007b5ace3440264dd0d5a Steven <steven.cohen714@gmail.com> 1745041050 +0200	reset: moving to origin/main
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a 5dd1ab6da18ef67ae45007b5ace3440264dd0d5a Steven <steven.cohen714@gmail.com> 1745057873 +0200	reset: moving to origin/main
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a 733ef8d6650df9b401c93a63914a204045d8d2ba Steven <steven.cohen714@gmail.com> 1745074823 +0200	commit: 📝 Auto-commit by script
733ef8d6650df9b401c93a63914a204045d8d2ba 30b856a09478eb5959cbb6be8f04fd5efcb2a5b4 Steven <steven.cohen714@gmail.com> 1745077079 +0200	commit: 📝 Auto-commit by script

```

### `.git/logs/refs/stash`
**(No description)**
```python
0000000000000000000000000000000000000000 f9f7b2b2944e045a63aded2db0abc9c69a8aa74b Steven <steven.cohen714@gmail.com> 1744525318 +0200	On main: Auto-stash for pull
f9f7b2b2944e045a63aded2db0abc9c69a8aa74b cab8db55d3595053898dd1edd40a1f31cc24761c Steven <steven.cohen714@gmail.com> 1745039269 +0200	On main: Auto-stash for pull

```

### `.git/logs/refs/heads/main`
**(No description)**
```python
0000000000000000000000000000000000000000 b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 Steven <steven.cohen714@gmail.com> 1743911110 +0200	commit (initial): Initial commit: Universal Recycling project
b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 Steven <steven.cohen714@gmail.com> 1743911697 +0200	Branch: renamed refs/heads/master to refs/heads/main
b502fe4efd22f26e6c8fa5805e5fc06dfe82b062 463dd88259cdc9a8a289f03e930db5e3ca01c059 Steven <steven.cohen714@gmail.com> 1743913278 +0200	commit (merge): Fix README merge conflict
463dd88259cdc9a8a289f03e930db5e3ca01c059 a22748f497f0a30fbfe7468c21e519a2887d295a Steven <steven.cohen714@gmail.com> 1743918421 +0200	commit: Fixed status capitalization in backend and frontend
a22748f497f0a30fbfe7468c21e519a2887d295a 4720170012386e15ee962e39c9d8272809da5eb8 Steven <steven.cohen714@gmail.com> 1743921810 +0200	commit: Updated files
4720170012386e15ee962e39c9d8272809da5eb8 7d4bf87e7208b0b536d5f4879bbcf4bace79763f Steven <steven.cohen714@gmail.com> 1744516215 +0200	reset: moving to origin/main
7d4bf87e7208b0b536d5f4879bbcf4bace79763f 0934f4eaf144035330f565464b89411da235a172 Steven <steven.cohen714@gmail.com> 1744518214 +0200	commit: Add GET /orders endpoint
0934f4eaf144035330f565464b89411da235a172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744525376 +0200	pull origin main: Fast-forward
b82c89c5571c7707f3d426c928ea247e8c2d7172 e28f74abef4ca5048cf1503f9a130554cf5970cf Steven <steven.cohen714@gmail.com> 1744530464 +0200	commit: Force sync scripts with correct names
e28f74abef4ca5048cf1503f9a130554cf5970cf 075eefe5307e9389ac202171d47ec626b84cb35c Steven <steven.cohen714@gmail.com> 1744860719 +0200	pull --rebase origin main: Fast-forward
075eefe5307e9389ac202171d47ec626b84cb35c a9adb8b6c85412eff2a43197f748b6d5dd9a8b6e Steven <steven.cohen714@gmail.com> 1744861041 +0200	commit: Resolved conflict in .DS_Store
a9adb8b6c85412eff2a43197f748b6d5dd9a8b6e 20d2770b6fecabeec22c38c28a289a18498ca7cd Steven <steven.cohen714@gmail.com> 1744861100 +0200	commit: Removed conflict junk in backend/endpoints/.DS_Store
20d2770b6fecabeec22c38c28a289a18498ca7cd 19b0d9fa6dbcbe8f9b08a709419372c8f445bc23 Steven <steven.cohen714@gmail.com> 1744899375 +0200	commit: Auto-commit for push (script)
19b0d9fa6dbcbe8f9b08a709419372c8f445bc23 acf94ac32d9a9d8e79d6ad1154d32675229ce6e0 Steven <steven.cohen714@gmail.com> 1744908994 +0200	commit: Auto-commit for push (script)
acf94ac32d9a9d8e79d6ad1154d32675229ce6e0 5dd1ab6da18ef67ae45007b5ace3440264dd0d5a Steven <steven.cohen714@gmail.com> 1744970528 +0200	commit: Auto-commit for push (script)
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a 733ef8d6650df9b401c93a63914a204045d8d2ba Steven <steven.cohen714@gmail.com> 1745074823 +0200	commit: 📝 Auto-commit by script
733ef8d6650df9b401c93a63914a204045d8d2ba 30b856a09478eb5959cbb6be8f04fd5efcb2a5b4 Steven <steven.cohen714@gmail.com> 1745077079 +0200	commit: 📝 Auto-commit by script

```

### `.git/logs/refs/remotes/origin/HEAD`
**(No description)**
```python
0000000000000000000000000000000000000000 7d4bf87e7208b0b536d5f4879bbcf4bace79763f Steven <steven.cohen714@gmail.com> 1744516215 +0200	fetch

```

### `.git/logs/refs/remotes/origin/main`
**(No description)**
```python
0000000000000000000000000000000000000000 d91e834bebf6b33871f3030ce35904cba271193a Steven <steven.cohen714@gmail.com> 1743913184 +0200	pull origin main --allow-unrelated-histories: storing head
d91e834bebf6b33871f3030ce35904cba271193a 463dd88259cdc9a8a289f03e930db5e3ca01c059 Steven <steven.cohen714@gmail.com> 1743913283 +0200	update by push
463dd88259cdc9a8a289f03e930db5e3ca01c059 a22748f497f0a30fbfe7468c21e519a2887d295a Steven <steven.cohen714@gmail.com> 1743918424 +0200	update by push
a22748f497f0a30fbfe7468c21e519a2887d295a 4720170012386e15ee962e39c9d8272809da5eb8 Steven <steven.cohen714@gmail.com> 1743921813 +0200	update by push
4720170012386e15ee962e39c9d8272809da5eb8 7d4bf87e7208b0b536d5f4879bbcf4bace79763f Steven <steven.cohen714@gmail.com> 1744516173 +0200	pull origin main: forced-update
7d4bf87e7208b0b536d5f4879bbcf4bace79763f 0934f4eaf144035330f565464b89411da235a172 Steven <steven.cohen714@gmail.com> 1744518251 +0200	update by push
0934f4eaf144035330f565464b89411da235a172 b82c89c5571c7707f3d426c928ea247e8c2d7172 Steven <steven.cohen714@gmail.com> 1744525183 +0200	pull origin main: fast-forward
b82c89c5571c7707f3d426c928ea247e8c2d7172 e28f74abef4ca5048cf1503f9a130554cf5970cf Steven <steven.cohen714@gmail.com> 1744530470 +0200	update by push
e28f74abef4ca5048cf1503f9a130554cf5970cf 075eefe5307e9389ac202171d47ec626b84cb35c Steven <steven.cohen714@gmail.com> 1744860719 +0200	pull --rebase origin main: fast-forward
075eefe5307e9389ac202171d47ec626b84cb35c 19b0d9fa6dbcbe8f9b08a709419372c8f445bc23 Steven <steven.cohen714@gmail.com> 1744899382 +0200	update by push
19b0d9fa6dbcbe8f9b08a709419372c8f445bc23 acf94ac32d9a9d8e79d6ad1154d32675229ce6e0 Steven <steven.cohen714@gmail.com> 1744909000 +0200	update by push
acf94ac32d9a9d8e79d6ad1154d32675229ce6e0 5dd1ab6da18ef67ae45007b5ace3440264dd0d5a Steven <steven.cohen714@gmail.com> 1744970535 +0200	update by push
5dd1ab6da18ef67ae45007b5ace3440264dd0d5a 733ef8d6650df9b401c93a63914a204045d8d2ba Steven <steven.cohen714@gmail.com> 1745074829 +0200	update by push
733ef8d6650df9b401c93a63914a204045d8d2ba 30b856a09478eb5959cbb6be8f04fd5efcb2a5b4 Steven <steven.cohen714@gmail.com> 1745077086 +0200	update by push

```

### `.git/hooks/applypatch-msg.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to check the commit log message taken by
# applypatch from an e-mail message.
#
# The hook should exit with non-zero status after issuing an
# appropriate message if it wants to stop the commit.  The hook is
# allowed to edit the commit message file.
#
# To enable this hook, rename this file to "applypatch-msg".

. git-sh-setup
commitmsg="$(git rev-parse --git-path hooks/commit-msg)"
test -x "$commitmsg" && exec "$commitmsg" ${1+"$@"}
:

```

### `.git/hooks/commit-msg.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to check the commit log message.
# Called by "git commit" with one argument, the name of the file
# that has the commit message.  The hook should exit with non-zero
# status after issuing an appropriate message if it wants to stop the
# commit.  The hook is allowed to edit the commit message file.
#
# To enable this hook, rename this file to "commit-msg".

# Uncomment the below to add a Signed-off-by line to the message.
# Doing this in a hook is a bad idea in general, but the prepare-commit-msg
# hook is more suited to it.
#
# SOB=$(git var GIT_AUTHOR_IDENT | sed -n 's/^\(.*>\).*$/Signed-off-by: \1/p')
# grep -qs "^$SOB" "$1" || echo "$SOB" >> "$1"

# This example catches duplicate Signed-off-by lines.

test "" = "$(grep '^Signed-off-by: ' "$1" |
	 sort | uniq -c | sed -e '/^[ 	]*1[ 	]/d')" || {
	echo >&2 Duplicate Signed-off-by lines.
	exit 1
}

```

### `.git/hooks/fsmonitor-watchman.sample`
**!/usr/bin/perl**
```python
#!/usr/bin/perl

use strict;
use warnings;
use IPC::Open2;

# An example hook script to integrate Watchman
# (https://facebook.github.io/watchman/) with git to speed up detecting
# new and modified files.
#
# The hook is passed a version (currently 2) and last update token
# formatted as a string and outputs to stdout a new update token and
# all files that have been modified since the update token. Paths must
# be relative to the root of the working tree and separated by a single NUL.
#
# To enable this hook, rename this file to "query-watchman" and set
# 'git config core.fsmonitor .git/hooks/query-watchman'
#
my ($version, $last_update_token) = @ARGV;

# Uncomment for debugging
# print STDERR "$0 $version $last_update_token\n";

# Check the hook interface version
if ($version ne 2) {
	die "Unsupported query-fsmonitor hook version '$version'.\n" .
	    "Falling back to scanning...\n";
}

my $git_work_tree = get_working_dir();

my $retry = 1;

my $json_pkg;
eval {
	require JSON::XS;
	$json_pkg = "JSON::XS";
	1;
} or do {
	require JSON::PP;
	$json_pkg = "JSON::PP";
};

launch_watchman();

sub launch_watchman {
	my $o = watchman_query();
	if (is_work_tree_watched($o)) {
		output_result($o->{clock}, @{$o->{files}});
	}
}

sub output_result {
	my ($clockid, @files) = @_;

	# Uncomment for debugging watchman output
	# open (my $fh, ">", ".git/watchman-output.out");
	# binmode $fh, ":utf8";
	# print $fh "$clockid\n@files\n";
	# close $fh;

	binmode STDOUT, ":utf8";
	print $clockid;
	print "\0";
	local $, = "\0";
	print @files;
}

sub watchman_clock {
	my $response = qx/watchman clock "$git_work_tree"/;
	die "Failed to get clock id on '$git_work_tree'.\n" .
		"Falling back to scanning...\n" if $? != 0;

	return $json_pkg->new->utf8->decode($response);
}

sub watchman_query {
	my $pid = open2(\*CHLD_OUT, \*CHLD_IN, 'watchman -j --no-pretty')
	or die "open2() failed: $!\n" .
	"Falling back to scanning...\n";

	# In the query expression below we're asking for names of files that
	# changed since $last_update_token but not from the .git folder.
	#
	# To accomplish this, we're using the "since" generator to use the
	# recency index to select candidate nodes and "fields" to limit the
	# output to file names only. Then we're using the "expression" term to
	# further constrain the results.
	my $last_update_line = "";
	if (substr($last_update_token, 0, 1) eq "c") {
		$last_update_token = "\"$last_update_token\"";
		$last_update_line = qq[\n"since": $last_update_token,];
	}
	my $query = <<"	END";
		["query", "$git_work_tree", {$last_update_line
			"fields": ["name"],
			"expression": ["not", ["dirname", ".git"]]
		}]
	END

	# Uncomment for debugging the watchman query
	# open (my $fh, ">", ".git/watchman-query.json");
	# print $fh $query;
	# close $fh;

	print CHLD_IN $query;
	close CHLD_IN;
	my $response = do {local $/; <CHLD_OUT>};

	# Uncomment for debugging the watch response
	# open ($fh, ">", ".git/watchman-response.json");
	# print $fh $response;
	# close $fh;

	die "Watchman: command returned no output.\n" .
	"Falling back to scanning...\n" if $response eq "";
	die "Watchman: command returned invalid output: $response\n" .
	"Falling back to scanning...\n" unless $response =~ /^\{/;

	return $json_pkg->new->utf8->decode($response);
}

sub is_work_tree_watched {
	my ($output) = @_;
	my $error = $output->{error};
	if ($retry > 0 and $error and $error =~ m/unable to resolve root .* directory (.*) is not watched/) {
		$retry--;
		my $response = qx/watchman watch "$git_work_tree"/;
		die "Failed to make watchman watch '$git_work_tree'.\n" .
		    "Falling back to scanning...\n" if $? != 0;
		$output = $json_pkg->new->utf8->decode($response);
		$error = $output->{error};
		die "Watchman: $error.\n" .
		"Falling back to scanning...\n" if $error;

		# Uncomment for debugging watchman output
		# open (my $fh, ">", ".git/watchman-output.out");
		# close $fh;

		# Watchman will always return all files on the first query so
		# return the fast "everything is dirty" flag to git and do the
		# Watchman query just to get it over with now so we won't pay
		# the cost in git to look up each individual file.
		my $o = watchman_clock();
		$error = $output->{error};

		die "Watchman: $error.\n" .
		"Falling back to scanning...\n" if $error;

		output_result($o->{clock}, ("/"));
		$last_update_token = $o->{clock};

		eval { launch_watchman() };
		return 0;
	}

	die "Watchman: $error.\n" .
	"Falling back to scanning...\n" if $error;

	return 1;
}

sub get_working_dir {
	my $working_dir;
	if ($^O =~ 'msys' || $^O =~ 'cygwin') {
		$working_dir = Win32::GetCwd();
		$working_dir =~ tr/\\/\//;
	} else {
		require Cwd;
		$working_dir = Cwd::cwd();
	}

	return $working_dir;
}

```

### `.git/hooks/post-update.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

exec git update-server-info

```

### `.git/hooks/pre-applypatch.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to verify what is about to be committed
# by applypatch from an e-mail message.
#
# The hook should exit with non-zero status after issuing an
# appropriate message if it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-applypatch".

. git-sh-setup
precommit="$(git rev-parse --git-path hooks/pre-commit)"
test -x "$precommit" && exec "$precommit" ${1+"$@"}
:

```

### `.git/hooks/pre-commit.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git commit" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message if
# it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-commit".

if git rev-parse --verify HEAD >/dev/null 2>&1
then
	against=HEAD
else
	# Initial commit: diff against an empty tree object
	against=$(git hash-object -t tree /dev/null)
fi

# If you want to allow non-ASCII filenames set this variable to true.
allownonascii=$(git config --type=bool hooks.allownonascii)

# Redirect output to stderr.
exec 1>&2

# Cross platform projects tend to avoid non-ASCII filenames; prevent
# them from being added to the repository. We exploit the fact that the
# printable range starts at the space character and ends with tilde.
if [ "$allownonascii" != "true" ] &&
	# Note that the use of brackets around a tr range is ok here, (it's
	# even required, for portability to Solaris 10's /usr/bin/tr), since
	# the square bracket bytes happen to fall in the designated range.
	test $(git diff-index --cached --name-only --diff-filter=A -z $against |
	  LC_ALL=C tr -d '[ -~]\0' | wc -c) != 0
then
	cat <<\EOF
Error: Attempt to add a non-ASCII file name.

This can cause problems if you want to work with people on other platforms.

To be portable it is advisable to rename the file.

If you know what you are doing you can disable this check using:

  git config hooks.allownonascii true
EOF
	exit 1
fi

# If there are whitespace errors, print the offending file names and fail.
exec git diff-index --check --cached $against --

```

### `.git/hooks/pre-merge-commit.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git merge" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message to
# stderr if it wants to stop the merge commit.
#
# To enable this hook, rename this file to "pre-merge-commit".

. git-sh-setup
test -x "$GIT_DIR/hooks/pre-commit" &&
        exec "$GIT_DIR/hooks/pre-commit"
:

```

### `.git/hooks/pre-push.sample`
**!/bin/sh**
```python
#!/bin/sh

# An example hook script to verify what is about to be pushed.  Called by "git
# push" after it has checked the remote status, but before anything has been
# pushed.  If this script exits with a non-zero status nothing will be pushed.
#
# This hook is called with the following parameters:
#
# $1 -- Name of the remote to which the push is being done
# $2 -- URL to which the push is being done
#
# If pushing without using a named remote those arguments will be equal.
#
# Information about the commits which are being pushed is supplied as lines to
# the standard input in the form:
#
#   <local ref> <local oid> <remote ref> <remote oid>
#
# This sample shows how to prevent push of commits where the log message starts
# with "WIP" (work in progress).

remote="$1"
url="$2"

zero=$(git hash-object --stdin </dev/null | tr '[0-9a-f]' '0')

while read local_ref local_oid remote_ref remote_oid
do
	if test "$local_oid" = "$zero"
	then
		# Handle delete
		:
	else
		if test "$remote_oid" = "$zero"
		then
			# New branch, examine all commits
			range="$local_oid"
		else
			# Update to existing branch, examine new commits
			range="$remote_oid..$local_oid"
		fi

		# Check for WIP commit
		commit=$(git rev-list -n 1 --grep '^WIP' "$range")
		if test -n "$commit"
		then
			echo >&2 "Found WIP commit in $local_ref, not pushing"
			exit 1
		fi
	fi
done

exit 0

```

### `.git/hooks/pre-rebase.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# Copyright (c) 2006, 2008 Junio C Hamano
#
# The "pre-rebase" hook is run just before "git rebase" starts doing
# its job, and can prevent the command from running by exiting with
# non-zero status.
#
# The hook is called with the following parameters:
#
# $1 -- the upstream the series was forked from.
# $2 -- the branch being rebased (or empty when rebasing the current branch).
#
# This sample shows how to prevent topic branches that are already
# merged to 'next' branch from getting rebased, because allowing it
# would result in rebasing already published history.

publish=next
basebranch="$1"
if test "$#" = 2
then
	topic="refs/heads/$2"
else
	topic=`git symbolic-ref HEAD` ||
	exit 0 ;# we do not interrupt rebasing detached HEAD
fi

case "$topic" in
refs/heads/??/*)
	;;
*)
	exit 0 ;# we do not interrupt others.
	;;
esac

# Now we are dealing with a topic branch being rebased
# on top of master.  Is it OK to rebase it?

# Does the topic really exist?
git show-ref -q "$topic" || {
	echo >&2 "No such branch $topic"
	exit 1
}

# Is topic fully merged to master?
not_in_master=`git rev-list --pretty=oneline ^master "$topic"`
if test -z "$not_in_master"
then
	echo >&2 "$topic is fully merged to master; better remove it."
	exit 1 ;# we could allow it, but there is no point.
fi

# Is topic ever merged to next?  If so you should not be rebasing it.
only_next_1=`git rev-list ^master "^$topic" ${publish} | sort`
only_next_2=`git rev-list ^master           ${publish} | sort`
if test "$only_next_1" = "$only_next_2"
then
	not_in_topic=`git rev-list "^$topic" master`
	if test -z "$not_in_topic"
	then
		echo >&2 "$topic is already up to date with master"
		exit 1 ;# we could allow it, but there is no point.
	else
		exit 0
	fi
else
	not_in_next=`git rev-list --pretty=oneline ^${publish} "$topic"`
	/usr/bin/perl -e '
		my $topic = $ARGV[0];
		my $msg = "* $topic has commits already merged to public branch:\n";
		my (%not_in_next) = map {
			/^([0-9a-f]+) /;
			($1 => 1);
		} split(/\n/, $ARGV[1]);
		for my $elem (map {
				/^([0-9a-f]+) (.*)$/;
				[$1 => $2];
			} split(/\n/, $ARGV[2])) {
			if (!exists $not_in_next{$elem->[0]}) {
				if ($msg) {
					print STDERR $msg;
					undef $msg;
				}
				print STDERR " $elem->[1]\n";
			}
		}
	' "$topic" "$not_in_next" "$not_in_master"
	exit 1
fi

<<\DOC_END

This sample hook safeguards topic branches that have been
published from being rewound.

The workflow assumed here is:

 * Once a topic branch forks from "master", "master" is never
   merged into it again (either directly or indirectly).

 * Once a topic branch is fully cooked and merged into "master",
   it is deleted.  If you need to build on top of it to correct
   earlier mistakes, a new topic branch is created by forking at
   the tip of the "master".  This is not strictly necessary, but
   it makes it easier to keep your history simple.

 * Whenever you need to test or publish your changes to topic
   branches, merge them into "next" branch.

The script, being an example, hardcodes the publish branch name
to be "next", but it is trivial to make it configurable via
$GIT_DIR/config mechanism.

With this workflow, you would want to know:

(1) ... if a topic branch has ever been merged to "next".  Young
    topic branches can have stupid mistakes you would rather
    clean up before publishing, and things that have not been
    merged into other branches can be easily rebased without
    affecting other people.  But once it is published, you would
    not want to rewind it.

(2) ... if a topic branch has been fully merged to "master".
    Then you can delete it.  More importantly, you should not
    build on top of it -- other people may already want to
    change things related to the topic as patches against your
    "master", so if you need further changes, it is better to
    fork the topic (perhaps with the same name) afresh from the
    tip of "master".

Let's look at this example:

		   o---o---o---o---o---o---o---o---o---o "next"
		  /       /           /           /
		 /   a---a---b A     /           /
		/   /               /           /
	       /   /   c---c---c---c B         /
	      /   /   /             \         /
	     /   /   /   b---b C     \       /
	    /   /   /   /             \     /
    ---o---o---o---o---o---o---o---o---o---o---o "master"


A, B and C are topic branches.

 * A has one fix since it was merged up to "next".

 * B has finished.  It has been fully merged up to "master" and "next",
   and is ready to be deleted.

 * C has not merged to "next" at all.

We would want to allow C to be rebased, refuse A, and encourage
B to be deleted.

To compute (1):

	git rev-list ^master ^topic next
	git rev-list ^master        next

	if these match, topic has not merged in next at all.

To compute (2):

	git rev-list master..topic

	if this is empty, it is fully merged to "master".

DOC_END

```

### `.git/hooks/pre-receive.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to make use of push options.
# The example simply echoes all push options that start with 'echoback='
# and rejects all pushes when the "reject" push option is used.
#
# To enable this hook, rename this file to "pre-receive".

if test -n "$GIT_PUSH_OPTION_COUNT"
then
	i=0
	while test "$i" -lt "$GIT_PUSH_OPTION_COUNT"
	do
		eval "value=\$GIT_PUSH_OPTION_$i"
		case "$value" in
		echoback=*)
			echo "echo from the pre-receive-hook: ${value#*=}" >&2
			;;
		reject)
			exit 1
		esac
		i=$((i + 1))
	done
fi

```

### `.git/hooks/prepare-commit-msg.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to prepare the commit log message.
# Called by "git commit" with the name of the file that has the
# commit message, followed by the description of the commit
# message's source.  The hook's purpose is to edit the commit
# message file.  If the hook fails with a non-zero status,
# the commit is aborted.
#
# To enable this hook, rename this file to "prepare-commit-msg".

# This hook includes three examples. The first one removes the
# "# Please enter the commit message..." help message.
#
# The second includes the output of "git diff --name-status -r"
# into the message, just before the "git status" output.  It is
# commented because it doesn't cope with --amend or with squashed
# commits.
#
# The third example adds a Signed-off-by line to the message, that can
# still be edited.  This is rarely a good idea.

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2
SHA1=$3

/usr/bin/perl -i.bak -ne 'print unless(m/^. Please enter the commit message/..m/^#$/)' "$COMMIT_MSG_FILE"

# case "$COMMIT_SOURCE,$SHA1" in
#  ,|template,)
#    /usr/bin/perl -i.bak -pe '
#       print "\n" . `git diff --cached --name-status -r`
# 	 if /^#/ && $first++ == 0' "$COMMIT_MSG_FILE" ;;
#  *) ;;
# esac

# SOB=$(git var GIT_COMMITTER_IDENT | sed -n 's/^\(.*>\).*$/Signed-off-by: \1/p')
# git interpret-trailers --in-place --trailer "$SOB" "$COMMIT_MSG_FILE"
# if test -z "$COMMIT_SOURCE"
# then
#   /usr/bin/perl -i.bak -pe 'print "\n" if !$first_line++' "$COMMIT_MSG_FILE"
# fi

```

### `.git/hooks/push-to-checkout.sample`
**!/bin/sh**
```python
#!/bin/sh

# An example hook script to update a checked-out tree on a git push.
#
# This hook is invoked by git-receive-pack(1) when it reacts to git
# push and updates reference(s) in its repository, and when the push
# tries to update the branch that is currently checked out and the
# receive.denyCurrentBranch configuration variable is set to
# updateInstead.
#
# By default, such a push is refused if the working tree and the index
# of the remote repository has any difference from the currently
# checked out commit; when both the working tree and the index match
# the current commit, they are updated to match the newly pushed tip
# of the branch. This hook is to be used to override the default
# behaviour; however the code below reimplements the default behaviour
# as a starting point for convenient modification.
#
# The hook receives the commit with which the tip of the current
# branch is going to be updated:
commit=$1

# It can exit with a non-zero status to refuse the push (when it does
# so, it must not modify the index or the working tree).
die () {
	echo >&2 "$*"
	exit 1
}

# Or it can make any necessary changes to the working tree and to the
# index to bring them to the desired state when the tip of the current
# branch is updated to the new commit, and exit with a zero status.
#
# For example, the hook can simply run git read-tree -u -m HEAD "$1"
# in order to emulate git fetch that is run in the reverse direction
# with git push, as the two-tree form of git read-tree -u -m is
# essentially the same as git switch or git checkout that switches
# branches while keeping the local changes in the working tree that do
# not interfere with the difference between the branches.

# The below is a more-or-less exact translation to shell of the C code
# for the default behaviour for git's push-to-checkout hook defined in
# the push_to_deploy() function in builtin/receive-pack.c.
#
# Note that the hook will be executed from the repository directory,
# not from the working tree, so if you want to perform operations on
# the working tree, you will have to adapt your code accordingly, e.g.
# by adding "cd .." or using relative paths.

if ! git update-index -q --ignore-submodules --refresh
then
	die "Up-to-date check failed"
fi

if ! git diff-files --quiet --ignore-submodules --
then
	die "Working directory has unstaged changes"
fi

# This is a rough translation of:
#
#   head_has_history() ? "HEAD" : EMPTY_TREE_SHA1_HEX
if git cat-file -e HEAD 2>/dev/null
then
	head=HEAD
else
	head=$(git hash-object -t tree --stdin </dev/null)
fi

if ! git diff-index --quiet --cached --ignore-submodules $head --
then
	die "Working directory has staged changes"
fi

if ! git read-tree -u -m "$commit"
then
	die "Could not update working tree to new HEAD"
fi

```

### `.git/hooks/sendemail-validate.sample`
**!/bin/sh**
```python
#!/bin/sh

# An example hook script to validate a patch (and/or patch series) before
# sending it via email.
#
# The hook should exit with non-zero status after issuing an appropriate
# message if it wants to prevent the email(s) from being sent.
#
# To enable this hook, rename this file to "sendemail-validate".
#
# By default, it will only check that the patch(es) can be applied on top of
# the default upstream branch without conflicts in a secondary worktree. After
# validation (successful or not) of the last patch of a series, the worktree
# will be deleted.
#
# The following config variables can be set to change the default remote and
# remote ref that are used to apply the patches against:
#
#   sendemail.validateRemote (default: origin)
#   sendemail.validateRemoteRef (default: HEAD)
#
# Replace the TODO placeholders with appropriate checks according to your
# needs.

validate_cover_letter () {
	file="$1"
	# TODO: Replace with appropriate checks (e.g. spell checking).
	true
}

validate_patch () {
	file="$1"
	# Ensure that the patch applies without conflicts.
	git am -3 "$file" || return
	# TODO: Replace with appropriate checks for this patch
	# (e.g. checkpatch.pl).
	true
}

validate_series () {
	# TODO: Replace with appropriate checks for the whole series
	# (e.g. quick build, coding style checks, etc.).
	true
}

# main -------------------------------------------------------------------------

if test "$GIT_SENDEMAIL_FILE_COUNTER" = 1
then
	remote=$(git config --default origin --get sendemail.validateRemote) &&
	ref=$(git config --default HEAD --get sendemail.validateRemoteRef) &&
	worktree=$(mktemp --tmpdir -d sendemail-validate.XXXXXXX) &&
	git worktree add -fd --checkout "$worktree" "refs/remotes/$remote/$ref" &&
	git config --replace-all sendemail.validateWorktree "$worktree"
else
	worktree=$(git config --get sendemail.validateWorktree)
fi || {
	echo "sendemail-validate: error: failed to prepare worktree" >&2
	exit 1
}

unset GIT_DIR GIT_WORK_TREE
cd "$worktree" &&

if grep -q "^diff --git " "$1"
then
	validate_patch "$1"
else
	validate_cover_letter "$1"
fi &&

if test "$GIT_SENDEMAIL_FILE_COUNTER" = "$GIT_SENDEMAIL_FILE_TOTAL"
then
	git config --unset-all sendemail.validateWorktree &&
	trap 'git worktree remove -ff "$worktree"' EXIT &&
	validate_series
fi

```

### `.git/hooks/update.sample`
**!/bin/sh**
```python
#!/bin/sh
#
# An example hook script to block unannotated tags from entering.
# Called by "git receive-pack" with arguments: refname sha1-old sha1-new
#
# To enable this hook, rename this file to "update".
#
# Config
# ------
# hooks.allowunannotated
#   This boolean sets whether unannotated tags will be allowed into the
#   repository.  By default they won't be.
# hooks.allowdeletetag
#   This boolean sets whether deleting tags will be allowed in the
#   repository.  By default they won't be.
# hooks.allowmodifytag
#   This boolean sets whether a tag may be modified after creation. By default
#   it won't be.
# hooks.allowdeletebranch
#   This boolean sets whether deleting branches will be allowed in the
#   repository.  By default they won't be.
# hooks.denycreatebranch
#   This boolean sets whether remotely creating branches will be denied
#   in the repository.  By default this is allowed.
#

# --- Command line
refname="$1"
oldrev="$2"
newrev="$3"

# --- Safety check
if [ -z "$GIT_DIR" ]; then
	echo "Don't run this script from the command line." >&2
	echo " (if you want, you could supply GIT_DIR then run" >&2
	echo "  $0 <ref> <oldrev> <newrev>)" >&2
	exit 1
fi

if [ -z "$refname" -o -z "$oldrev" -o -z "$newrev" ]; then
	echo "usage: $0 <ref> <oldrev> <newrev>" >&2
	exit 1
fi

# --- Config
allowunannotated=$(git config --type=bool hooks.allowunannotated)
allowdeletebranch=$(git config --type=bool hooks.allowdeletebranch)
denycreatebranch=$(git config --type=bool hooks.denycreatebranch)
allowdeletetag=$(git config --type=bool hooks.allowdeletetag)
allowmodifytag=$(git config --type=bool hooks.allowmodifytag)

# check for no description
projectdesc=$(sed -e '1q' "$GIT_DIR/description")
case "$projectdesc" in
"Unnamed repository"* | "")
	echo "*** Project description file hasn't been set" >&2
	exit 1
	;;
esac

# --- Check types
# if $newrev is 0000...0000, it's a commit to delete a ref.
zero=$(git hash-object --stdin </dev/null | tr '[0-9a-f]' '0')
if [ "$newrev" = "$zero" ]; then
	newrev_type=delete
else
	newrev_type=$(git cat-file -t $newrev)
fi

case "$refname","$newrev_type" in
	refs/tags/*,commit)
		# un-annotated tag
		short_refname=${refname##refs/tags/}
		if [ "$allowunannotated" != "true" ]; then
			echo "*** The un-annotated tag, $short_refname, is not allowed in this repository" >&2
			echo "*** Use 'git tag [ -a | -s ]' for tags you want to propagate." >&2
			exit 1
		fi
		;;
	refs/tags/*,delete)
		# delete tag
		if [ "$allowdeletetag" != "true" ]; then
			echo "*** Deleting a tag is not allowed in this repository" >&2
			exit 1
		fi
		;;
	refs/tags/*,tag)
		# annotated tag
		if [ "$allowmodifytag" != "true" ] && git rev-parse $refname > /dev/null 2>&1
		then
			echo "*** Tag '$refname' already exists." >&2
			echo "*** Modifying a tag is not allowed in this repository." >&2
			exit 1
		fi
		;;
	refs/heads/*,commit)
		# branch
		if [ "$oldrev" = "$zero" -a "$denycreatebranch" = "true" ]; then
			echo "*** Creating a branch is not allowed in this repository" >&2
			exit 1
		fi
		;;
	refs/heads/*,delete)
		# delete branch
		if [ "$allowdeletebranch" != "true" ]; then
			echo "*** Deleting a branch is not allowed in this repository" >&2
			exit 1
		fi
		;;
	refs/remotes/*,commit)
		# tracking branch
		;;
	refs/remotes/*,delete)
		# delete tracking branch
		if [ "$allowdeletebranch" != "true" ]; then
			echo "*** Deleting a tracking branch is not allowed in this repository" >&2
			exit 1
		fi
		;;
	*)
		# Anything else (is there anything else?)
		echo "*** Update hook: unknown type of update to ref $refname of type $newrev_type" >&2
		exit 1
		;;
esac

# --- Finished
exit 0

```

### `.git/refs/stash`
**(No description)**
```python
cab8db55d3595053898dd1edd40a1f31cc24761c

```

### `.git/refs/heads/main`
**(No description)**
```python
30b856a09478eb5959cbb6be8f04fd5efcb2a5b4

```

### `.git/refs/remotes/origin/HEAD`
**(No description)**
```python
ref: refs/remotes/origin/main

```

### `.git/refs/remotes/origin/main`
**(No description)**
```python
30b856a09478eb5959cbb6be8f04fd5efcb2a5b4

```

### `data/orders.db`
**(No description)**
```python
<!-- ERROR reading orders.db: 'utf-8' codec can't decode byte 0x86 in position 98: invalid start byte -->
```

### `data/test_orders.db`
**(No description)**
```python
<!-- ERROR reading test_orders.db: 'utf-8' codec can't decode byte 0x86 in position 98: invalid start byte -->
```

### `data/uploads/20_test_invoice.pdf`
**(No description)**
```python
Dummy content for pipeline test
```

### `data/uploads/21_test_invoice.pdf`
**(No description)**
```python
Dummy PDF content
```

### `data/uploads/test_invoice.pdf`
**(No description)**
```python
Dummy content for pipeline test
```

### `data/printouts/order_1.txt`
**(No description)**
```python
Order Number: PO002
Status: Pending
Created Date: 2025-04-17T09:53:39.614927
Received Date: None
Total: 29.97
Order Note: Shell test order
Supplier Note: Test supplier
Requester: Aaron

Line Items:
-----------
Item Code: TEST123
Description: Integration Widget
Project: TEST
Qty: 3.0
Price: 9.99
Total: 29.97


```

### `data/printouts/order_3.txt`
**(No description)**
```python
order_number: PO_TEST_001
status: Received
created_date: 2025-04-13T13:24:38.837327
received_date: 2025-04-13T14:18:43.917109
total: 999.99
order_note: This is a test order note
supplier_note: This is a supplier note
requester: Steven

Line Items:
-----------
item_code: TEST001
item_description: Test Widget A
project: Project A
qty_ordered: 3
price: 100.0
total: 300.0

item_code: TEST002
item_description: Test Widget B
project: Project B
qty_ordered: 2
price: 349.99
total: 699.99


```

### `data/printouts/order_7.txt`
**(No description)**
```python
Order Number: PO_TESTA1
Status: Awaiting Authorisation
Created Date: 2025-04-17T15:37:12.567632
Received Date: None
Total: 14000.0
Order Note: High Value Order 1
Note to Supplier: Needs urgent approval
Requester: Aaron

Line Items:
-----------
Item Code: ITM003
Description: Pump
Project: PRO003
Qty: 2.0
Price: 6000.0
Total: 12000.0

Item Code: ITM001
Description: Valve
Project: PRO001
Qty: 1.0
Price: 2000.0
Total: 2000.0


```

## 🗄️ Database Schema (`data/orders.db`)

_Tracks all purchase orders through Pending→Received states, plus lookup tables & audit logs._

### Table `requesters`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `name` (TEXT), pk=False, notnull=False, default=None

### Table `sqlite_sequence`
- `name` (), pk=False, notnull=False, default=None
- `seq` (), pk=False, notnull=False, default=None

### Table `suppliers`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `account_number` (TEXT), pk=False, notnull=False, default=None
- `name` (TEXT), pk=False, notnull=False, default=None
- `telephone` (TEXT), pk=False, notnull=False, default=None
- `vat_number` (TEXT), pk=False, notnull=False, default=None
- `registration_number` (TEXT), pk=False, notnull=False, default=None
- `email` (TEXT), pk=False, notnull=False, default=None
- `contact_name` (TEXT), pk=False, notnull=False, default=None
- `contact_telephone` (TEXT), pk=False, notnull=False, default=None
- `address_line1` (TEXT), pk=False, notnull=False, default=None
- `address_line2` (TEXT), pk=False, notnull=False, default=None
- `address_line3` (TEXT), pk=False, notnull=False, default=None
- `postal_code` (TEXT), pk=False, notnull=False, default=None

### Table `orders`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_number` (TEXT), pk=False, notnull=False, default=None
- `status` (TEXT), pk=False, notnull=False, default=None
- `created_date` (TEXT), pk=False, notnull=False, default=CURRENT_TIMESTAMP
- `received_date` (TEXT), pk=False, notnull=False, default=None
- `total` (REAL), pk=False, notnull=False, default=None
- `order_note` (TEXT), pk=False, notnull=False, default=None
- `note_to_supplier` (TEXT), pk=False, notnull=False, default=None
- `supplier_id` (INTEGER), pk=False, notnull=False, default=None
- `requester_id` (INTEGER), pk=False, notnull=False, default=None

### Table `order_items`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_id` (INTEGER), pk=False, notnull=False, default=None
- `item_code` (TEXT), pk=False, notnull=False, default=None
- `item_description` (TEXT), pk=False, notnull=False, default=None
- `project` (TEXT), pk=False, notnull=False, default=None
- `qty_ordered` (REAL), pk=False, notnull=False, default=None
- `qty_received` (REAL), pk=False, notnull=False, default=None
- `received_date` (TEXT), pk=False, notnull=False, default=None
- `price` (REAL), pk=False, notnull=False, default=None
- `total` (REAL), pk=False, notnull=False, default=None

### Table `attachments`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_id` (INTEGER), pk=False, notnull=False, default=None
- `filename` (TEXT), pk=False, notnull=True, default=None
- `file_path` (TEXT), pk=False, notnull=True, default=None
- `upload_date` (TEXT), pk=False, notnull=True, default=None

### Table `audit_trail`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `order_id` (INTEGER), pk=False, notnull=False, default=None
- `action` (TEXT), pk=False, notnull=False, default=None
- `details` (TEXT), pk=False, notnull=False, default=None
- `action_date` (TEXT), pk=False, notnull=False, default=CURRENT_TIMESTAMP
- `user_id` (INTEGER), pk=False, notnull=False, default=None

### Table `settings`
- `key` (TEXT), pk=True, notnull=False, default=None
- `value` (TEXT), pk=False, notnull=False, default=None

### Table `users`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `username` (TEXT), pk=False, notnull=False, default=None
- `password_hash` (TEXT), pk=False, notnull=True, default=None
- `rights` (TEXT), pk=False, notnull=True, default=None

### Table `projects`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `project_code` (TEXT), pk=False, notnull=False, default=None
- `project_name` (TEXT), pk=False, notnull=False, default=None

### Table `items`
- `id` (INTEGER), pk=True, notnull=False, default=None
- `item_code` (TEXT), pk=False, notnull=False, default=None
- `item_description` (TEXT), pk=False, notnull=False, default=None


## 📝 Project summary
I am busy building a Purchase Order system for Universal Recycling.

**Testing Methodology:**
- Each feature is tested in isolation (Python scripts, curl, direct sqlite3 queries)
- No feature gets built on top of another until the one before it passes
- Audit trails, status transitions, and data integrity are tested at every step
- Test records are inserted programmatically, not by hand
- UI will only be added when backend is rock solid

**File Structure Summary:**
- `backend/endpoints/orders.py` → Handles all `/orders` routes
- `backend/database.py` → DB operations: init, insert, queries
- `backend/utils/order_utils.py` → Helpers: status logic, validation
- `scripts/` → Injection scripts, test runners & setup tools
- `frontend/templates/` → Screen layouts (planned)
- `data/orders.db` → Active SQLite file

**Build Methodology:**
- Build backend first → fully tested
- One feature at a time → injected via `.py` scripts
- No UI work until backend is rock solid
- All tests confirmed via curl + Python
- Full end-to-end integration test exists
- Code reusability is a must (e.g. date handling, filters)

**How Steven works with ChatGPT:**
- Steven doesn’t know coding; he’s decent with terminal commands
- He uses VS Code, wants brief error messages & clear steps


## 🔐 Users & Roles

| Username | Role  |
|----------|-------|
| Steven   | Admin |
| Aaron    | Edit  |
| Yolandi  | View  |

Passwords are hashed; assumed defaults for local testing: `password`.

## ⚙️ System Settings

| Key                 | Value   |
|----------------------|---------|
| auth_threshold       | 10000   |
| order_number_start   | URC1024 |
| last_order_number    | URC000  |

## 🚦 FastAPI Endpoint Summary

| Endpoint                     | Method    | Status         |
|------------------------------|-----------|----------------|
| `/orders`                   | POST      | ✅ Implemented |
| `/orders/receive`           | POST      | ✅ Implemented |
| `/orders/next_order_number` | GET       | ✅ Implemented |
| `/attachments/upload`       | POST      | ✅ Implemented |
| `/notes`                    | GET/POST  | ✅ Implemented |
| `/audit`                    | GET       | ⏳ Pending     |
| `/orders/print`             | GET       | ⏳ Planned     |
| `/lookups/suppliers`        | GET       | ✅ Implemented |
| `/lookups/requesters`       | GET       | ✅ Implemented |
| `/lookups/projects`         | GET       | ✅ Implemented |
| `/lookups/items`            | GET       | ✅ Implemented |

## 🧪 Test Coverage Summary

| Test Script | Purpose | Status |
|-------------|---------|--------|
| `test_authorisation_threshold_trigger.py` | High-value order triggers auth flow | ✅ |
| `test_invalid_data_handling.py` | Ensures invalid payloads return 422/400 | ✅ |
| `test_invalid_items_variants.py` | Covers malformed line item edge cases | ✅ |
| `test_pipeline_end_to_end.py` | Full pipeline test: creation → receive | ✅ |
| `test_receive_partial.py` | Tests partial receiving with audit tracking | ✅ |

