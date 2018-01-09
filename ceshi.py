#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url = 'https://www.okex.com/api/v1/future_ticker.do'
foo = 'ace_btc,ace_eth,ace_usdt,act_bch,act_btc,act_eth,act_usdt,amm_btc,amm_eth,amm_usdt,ark_btc,ark_eth,ark_usdt,ast_btc,ast_eth,ast_usdt,avt_bch,avt_btc,avt_eth,avt_usdt,bcd_bch,bcd_btc,bcd_usdt,bch_btc,bch_usdt,bcx_bch,bcx_btc,bnt_btc,bnt_eth,bnt_usdt,btc_usdt,btg_bch,btg_btc,btg_usdt,btm_btc,btm_eth,btm_usdt,bt2_btc,cmt_bch,cmt_btc,cmt_eth,cmt_usdt,ctr_btc,ctr_eth,ctr_usdt,cvc_btc,cvc_eth,cvc_usdt,dash_bch,dash_btc,dash_eth,dash_usdt,dat_btc,dat_eth,dat_usdt,dgb_btc,dgb_eth,dgb_usdt,dgd_bch,dgd_btc,dgd_eth,dgd_usdt,dnt_btc,dnt_eth,dnt_usdt,dpy_btc,dpy_eth,dpy_usdt,edo_bch,edo_btc,edo_eth,edo_usdt,elf_btc,elf_eth,elf_usdt,eng_btc,eng_eth,eng_usdt,eos_bch,eos_btc,eos_eth,eos_usdt,etc_bch,etc_btc,etc_eth,etc_usdt,eth_btc,eth_usdt,evx_btc,evx_eth,evx_usdt,fun_btc,fun_eth,fun_usdt,gas_btc,gas_eth,gas_usdt,gnt_btc,gnt_eth,gnt_usdt,gnx_btc,gnx_eth,gnx_usdt,hsr_btc,hsr_eth,hsr_usdt,icn_btc,icn_eth,icn_usdt,icx_btc,icx_eth,icx_usdt,iota_btc,iota_eth,iota_usdt,itc_btc,itc_eth,itc_usdt,kcash_btc,kcash_eth,kcash_usdt,knc_btc,knc_eth,knc_usdt,link_btc,link_eth,link_usdt,lrc_btc,lrc_eth,lrc_usdt,ltc_bch,ltc_btc,ltc_eth,ltc_usdt,mana_btc,mana_eth,mana_usdt,mco_btc,mco_eth,mco_usdt,mda_btc,mda_eth,mda_usdt,mdt_btc,mdt_eth,mdt_usdt,mth_btc,mth_eth,mth_usdt,mtl_btc,mtl_eth,mtl_usdt,nas_btc,nas_eth,nas_usdt,neo_btc,neo_eth,neo_usdt,nuls_btc,nuls_eth,nuls_usdt,oax_btc,oax_eth,oax_usdt,omg_btc,omg_eth,omg_usdt,pay_btc,pay_eth,pay_usdt,ppt_btc,ppt_eth,ppt_usdt,pro_btc,pro_eth,pro_usdt,qtum_btc,qtum_eth,qtum_usdt,qvt_btc,qvt_eth,qvt_usdt,rcn_btc,rcn_eth,rcn_usdt,rdn_btc,rdn_eth,rdn_usdt,read_btc,read_eth,read_usdt,req_btc,req_eth,req_usdt,rnt_btc,rnt_eth,rnt_usdt,salt_btc,salt_eth,salt_usdt,san_btc,san_eth,san_usdt,sbtc_bch,sbtc_btc,sngls_btc,sngls_eth,sngls_usdt,snm_btc,snm_eth,snm_usdt,snt_btc,snt_eth,snt_usdt,ssc_btc,ssc_eth,ssc_usdt,storj_btc,storj_eth,storj_usdt,sub_btc,sub_eth,sub_usdt,swftc_btc,swftc_eth,swftc_usdt,tnb_btc,tnb_eth,tnb_usdt,trx_btc,trx_eth,trx_usdt,ugc_btc,ugc_eth,ugc_usdt,ukg_btc,ukg_eth,ukg_usdt,vee_btc,vee_eth,vee_usdt,wrc_btc,wrc_eth,wrc_usdt,wtc_btc,wtc_eth,wtc_usdt,xem_btc,xem_eth,xem_usdt,xlm_btc,xlm_eth,xlm_usdt,xmr_btc,xmr_eth,xmr_usdt,xrp_btc,xrp_eth,xrp_usdt,xuc_btc,xuc_eth,xuc_usdt,yoyo_btc,yoyo_eth,yoyo_usdt,zec_btc,zec_eth,zec_usdt,zrx_btc,zrx_eth,zrx_usdt,1st_btc,1st_eth,1st_usdt'

foo_list = foo.split(',')

for each in foo_list:
    payload = {'symbol': each, 'contract_type': 'this_week'}
    response = requests.get(url, params=payload)
    print(response.url)
    print(response.json())