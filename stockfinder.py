# Develop a scanner to identify stocks that have reached a lifetime high, used that high as a strong support level, and then experienced significant price appreciation. Analyze data from the last 10 years to determine how often this occurred, the annual opportunities, and the scanner's success rate.

#dataset downloaded from https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the CSV file containing NSE stocks
def load_nse_stocks(csv_file):
    return pd.read_csv(csv_file)

# Function to fetch stock data using yfinance
def fetch_stock_data(ticker, period='10y'):
    try:
        data = yf.Ticker(ticker).history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Function to identify lifetime high and check for support and appreciation
def identify_lifetime_high_and_support(data, support_threshold=0.25, appreciation_threshold=0.10):
    lifetime_high = data['High'].max()
    lifetime_high_date = data['High'].idxmax()
    
    # Data after reaching lifetime high
    post_high_data = data[lifetime_high_date:]
    pullback_low = post_high_data['Low'].min()
    
    # Check if pullback low is within support threshold
    if (lifetime_high - pullback_low) / lifetime_high < support_threshold:
        # Check for significant price appreciation after pullback
        post_pullback_data = post_high_data[post_high_data.index > post_high_data['Low'].idxmin()]
        if post_pullback_data['Close'].max() / pullback_low > (1 + appreciation_threshold):
            return True, lifetime_high, pullback_low, post_pullback_data['Close'].max()
        else:
            return False, None, None, None
    else:
        return False, None, None, None

# Function to analyze and report on each stock
def analyze_and_report_stocks(stocks_df):
    results = []
    failed_tickers = []
    annual_opportunities = {}
    
    # Create a directory for saving graphs
    os.makedirs('StockGraphs', exist_ok=True)
    
    for index, row in stocks_df.iterrows():
        ticker = row['SYMBOL'].strip() + '.NS'
        print(f"Analyzing {ticker}...")
        data = fetch_stock_data(ticker)
        
        # If no data is available, skip the ticker
        if data is None or data.empty:
            print(f"No data available for {ticker}")
            failed_tickers.append(ticker)
            continue
        
        # Apply criteria to identify valid stocks
        result, lifetime_high, pullback_low, appreciation_high = identify_lifetime_high_and_support(data)
        
        if result:
            print(f"Stock {ticker} met the criteria:")
            print(f"  - Lifetime High: {lifetime_high}")
            print(f"  - Pullback Low: {pullback_low}")
            print(f"  - Appreciation High: {appreciation_high}")
            results.append({
                'Ticker': ticker,
                'Lifetime High': lifetime_high,
                'Pullback Low': pullback_low,
                'Appreciation High': appreciation_high
            })
            
            # Record the year of opportunity
            year = data.index[-1].year  # Use the last date in the data for the year
            if year in annual_opportunities:
                annual_opportunities[year] += 1
            else:
                annual_opportunities[year] = 1
            
            # Save the stock's history to visualize
            plt.figure(figsize=(10, 5))
            plt.plot(data['Close'], label='Close Price')
            plt.axhline(y=lifetime_high, color='r', linestyle='--', label='Lifetime High')
            plt.axhline(y=pullback_low, color='g', linestyle='--', label='Pullback Low')
            plt.legend()
            plt.title(f"{ticker} Price History")
            plt.xlabel('Date')
            plt.ylabel('Price')
            
            # Save the plot as an image
            plt.savefig(f'StockGraphs/{ticker}.png')
            plt.close()  # Close the plot to avoid display
            
        else:
            print(f"Stock {ticker} did not meet the criteria.")
    
    # Convert results to DataFrame for analysis
    results_df = pd.DataFrame(results)
    return results_df, failed_tickers, annual_opportunities

# Example usage
csv_file = 'NSElist.csv'  # Replace with the actual path to your CSV file containing NSE stock symbols
nse_stocks = load_nse_stocks(csv_file)
results_df, failed_tickers, annual_opportunities = analyze_and_report_stocks(nse_stocks)

# Save the results to a CSV file
results_df.to_csv('stock_scanner_results.csv', index=False)
print("Analysis complete. Results saved to 'stock_scanner_results.csv'.")

# Calculate and print the success rate
total_stocks = len(nse_stocks)
successful_stocks = len(results_df)
if total_stocks > 0:
    success_rate = (successful_stocks / total_stocks) * 100
    print(f"Success Rate: {success_rate:.2f}%")
else:
    print("No stocks to analyze.")

# Print annual opportunities
print("Annual Opportunities:")
for year, count in annual_opportunities.items():
    print(f"  {year}: {count} opportunities")
    
print("Failed Tickers:", failed_tickers)

# output:
# Analysis complete. Results saved to 'stock_scanner_results.csv'.
# Success Rate: 8.06%
# Annual Opportunities:
#   2024: 163 opportunities
# Failed Tickers: ['AAATECH.NS', 'AADHARHFC.NS', 'AAREYDRUGS.NS', 'AARTECH.NS', 'AARTIPHARM.NS', 'AARTISURF.NS', 'ABDL.NS', 'ABSLAMC.NS', 'ACI.NS', 'ADANIENSOL.NS', 'ADL.NS', 'AEGISLOG.NS', 'AEROFLEX.NS', 'AETHER.NS', 'AFIL.NS', 'AGIIL.NS', 'AGSTRA.NS', 'AHL.NS', 'AIIL.NS', 'AKI.NS', 'AKSHAR.NS', 'AKUMS.NS', 'ALLDIGI.NS', 'AMIORG.NS', 'AMNPLST.NS', 'ANANDRATHI.NS', 'ANGELONE.NS', 'ANMOL.NS', 'ANURAS.NS', 'APOLLOPIPE.NS', 'APTUS.NS', 'ARE&M.NS', 'ARIHANTCAP.NS', 'ARKADE.NS', 'ARTEMISMED.NS', 'ASALCBR.NS', 'ASHOKAMET.NS', 'ASIANENE.NS', 'ASKAUTOLTD.NS', 'ATALREAL.NS', 'ATAM.NS', 'ATL.NS', 'AVALON.NS', 'AVANTEL.NS', 'AVONMORE.NS', 'AWFIS.NS', 'AWHCL.NS', 'AWL.NS', 'AXITA.NS', 'AZAD.NS', 'BAIDFIN.NS', 'BAJAJHCARE.NS', 'BAJAJHFL.NS', 'BAJEL.NS', 'BALAJEE.NS', 'BALUFORGE.NS', 'BANSALWIRE.NS', 'BARBEQUE.NS', 'BCLIND.NS', 'BECTORFOOD.NS', 'BESTAGRO.NS', 'BHAGCHEM.NS', 'BHARTIHEXA.NS', 'BIKAJI.NS', 'BLAL.NS', 'BLSE.NS', 'BLUEJET.NS', 'BOROLTD.NS', 'BOROSCI.NS', 'BTML.NS', 'CAMPUS.NS', 'CAMS.NS', 'CAPITALSFB.NS', 'CARTRADE.NS', 'CARYSIL.NS', 'CEIGALL.NS', 'CELLO.NS', 'CHEMBOND.NS', 'CHEMCON.NS', 'CHEMPLASTS.NS', 'CHEVIOT.NS', 'CHOICEIN.NS', 'CLEAN.NS', 'CLSEL.NS', 'CMSINFO.NS', 'COASTCORP.NS', 'COMSYN.NS', 'CONCORDBIO.NS', 'CONFIPET.NS', 'CRAFTSMAN.NS', 'CSBBANK.NS', 'CSLFINANCE.NS', 'CYIENTDLM.NS', 'DATAPATTNS.NS', 'DAVANGERE.NS', 'DBOL.NS', 'DCI.NS', 'DCMSRIND.NS', 'DCXINDIA.NS', 'DEEDEV.NS', 'DEEPINDS.NS', 'DELHIVERY.NS', 'DEVYANI.NS', 'DHARMAJ.NS', 'DHRUV.NS', 'DIAMINESQ.NS', 'DIFFNKG.NS', 'DIGIDRIVE.NS', 'DIVGIITTS.NS', 'DJML.NS', 'DMCC.NS', 'DODLA.NS', 'DOMS.NS', 'DRCSYSTEMS.NS', 'DREAMFOLKS.NS', 'DYCL.NS', 'EASEMYTRIP.NS', 'ECOSMOBLTY.NS', 'ELDEHSG.NS', 'ELIN.NS', 'EMBDL.NS', 'EMCURE.NS', 'EMIL.NS', 'EMSLIMITED.NS', 'EMUDHRA.NS', 'ENTERO.NS', 'EPACK.NS', 'EPIGRAL.NS', 'EQUITASBNK.NS', 'ESAFSFB.NS', 'ETHOSLTD.NS', 'EUREKAFORB.NS', 'EXICOM.NS', 'EXXARO.NS', 'FAIRCHEMOR.NS', 'FAZE3Q.NS', 'FEDFINA.NS', 'FIBERWEB.NS', 'FILATFASH.NS', 'FINOPB.NS', 'FIRSTCRY.NS', 'FIVESTAR.NS', 'FLAIR.NS', 'FOODSIN.NS', 'FUSION.NS', 'GALAPREC.NS', 'GANDHAR.NS', 'GANESHBE.NS', 'GATECH.NS', 'GATECHDVR.NS', 'GATEWAY.NS', 'GENCON.NS', 'GENSOL.NS', 'GHCLTEXTIL.NS', 'GLAND.NS', 'GLOBALE.NS', 'GLOSTERLTD.NS', 'GLS.NS', 'GMRP&UI.NS', 'GOCOLORS.NS', 'GODIGIT.NS', 'GOPAL.NS', 'GOYALALUM.NS', 'GPTHEALTH.NS', 'GREENPANEL.NS', 'GRINFRA.NS', 'GRMOVER.NS', 'GRWRHITECH.NS', 'GSLSU.NS', 'GTECJAINX.NS', 'HAPPSTMNDS.NS', 'HAPPYFORGE.NS', 'HARDWYN.NS', 'HARIOMPIPE.NS', 'HARSHA.NS', 'HEMIPROP.NS', 'HERANBA.NS', 'HINDWAREAP.NS', 'HLEGLAS.NS', 'HMAAGRO.NS', 'HNDFDS.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HPAL.NS', 'HPIL.NS', 'HYBRIDFIN.NS', 'ICDSLTD.NS', 'IDEAFORGE.NS', 'IEL.NS', 'IKIO.NS', 'INDGN.NS', 'INDIASHLTR.NS', 'INDIGOPNTS.NS', 'INDOAMIN.NS', 'INDOBORAX.NS', 'INDOUS.NS', 'INNOVACAP.NS', 'INOXGREEN.NS', 'INOXINDIA.NS', 'INTERARCH.NS', 'INTLCONV.NS', 'IONEXCHANG.NS', 'IPL.NS', 'IREDA.NS', 'IRFC.NS', 'IRIS.NS', 'IRMENERGY.NS', 'ISGEC.NS', 'IWEL.NS', 'IXIGO.NS', 'JGCHEM.NS', 'JIOFIN.NS', 'JLHL.NS', 'JNKINDIA.NS', 'JSFB.NS', 'JSWINFRA.NS', 'JTLIND.NS', 'JUBLINGREA.NS', 'JUNIPER.NS', 'JYOTICNC.NS', 'KALAMANDIR.NS', 'KALYANI.NS', 'KALYANKJIL.NS', 'KAMOPAINTS.NS', 'KANPRPLA.NS', 'KAYNES.NS', 'KEEPLEARN.NS', 'KFINTECH.NS', 'KHAICHEM.NS', 'KIMS.NS', 'KIRLPNU.NS', 'KPIGREEN.NS', 'KPIL.NS', 'KRITINUT.NS', 'KRN.NS', 'KRONOX.NS', 'KROSS.NS', 'KRSNAA.NS', 'KRYSTAL.NS', 'KSOLVES.NS', 'KUANTUM.NS', 'LAL.NS', 'LANCORHOL.NS', 'LANDMARK.NS', 'LATENTVIEW.NS', 'LGHL.NS', 'LICI.NS', 'LIKHITHA.NS', 'LLOYDSENGG.NS', 'LLOYDSME.NS', 'LODHA.NS', 'LORDSCHLO.NS', 'LOYALTEX.NS', 'LTFOODS.NS', 'LXCHEM.NS', 'MAHEPC.NS', 'MALLCOM.NS', 'MANBA.NS', 'MANCREDIT.NS', 'MANKIND.NS', 'MANOMAY.NS', 'MANORAMA.NS', 'MANORG.NS', 'MANYAVAR.NS', 'MAPMYINDIA.NS', 'MAXESTATES.NS', 'MAXHEALTH.NS', 'MAXIND.NS', 'MAZDOCK.NS', 'MEDANTA.NS', 'MEDIASSIST.NS', 'MEDICAMEQ.NS', 'MEDICO.NS', 'MEDPLUS.NS', 'MEGASTAR.NS', 'METROBRAND.NS', 'MFML.NS', 'MGEL.NS', 'MHLXMIRU.NS', 'MITTAL-RE1.NS', 'MODISONLTD.NS', 'MODTHREAD.NS', 'MOL.NS', 'MONARCH.NS', 'MOTISONS.NS', 'MSUMI.NS', 'MTARTECH.NS', 'MUFIN.NS', 'MUFTI.NS', 'MUKKA.NS', 'MUTHOOTMF.NS', 'MVGJL.NS', 'NAZARA.NS', 'NDLVENTURE.NS', 'NDRAUTO.NS', 'NETWEB.NS', 'NGIL.NS', 'NGLFINE.NS', 'NIITMTS.NS', 'NINSYS.NS', 'NIRAJ.NS', 'NIRAJISPAT.NS', 'NORTHARC.NS', 'NOVAAGRI.NS', 'NRL.NS', 'NSLNISP.NS', 'NURECA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'NYKAA.NS', 'OAL.NS', 'OBCL.NS', 'OLAELEC.NS', 'ORIENTCER.NS', 'ORIENTTECH.NS', 'ORTINGLOBE.NS', 'PAKKA.NS', 'PARADEEP.NS', 'PARAS.NS', 'PARKHOTELS.NS', 'PASUPTAC.NS', 'PAVNAIND.NS', 'PAYTM.NS', 'PIXTRANS.NS', 'PLATIND.NS', 'PLAZACABLE.NS', 'PNGJL.NS', 'POLICYBZR.NS', 'POWERINDIA.NS', 'PPLPHARMA.NS', 'PREMIERENE.NS', 'PRINCEPIPE.NS', 'PRITIKAUTO.NS', 'PRUDENT.NS', 'PRUDMOULI.NS', 'PTCIL.NS', 'PVRINOX.NS', 'PVSL.NS', 'PYRAMID.NS', 'RACE.NS', 'RADHIKAJWE.NS', 'RADIANTCMS.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RAJRATAN.NS', 'RAMAPHO.NS', 'RAMRAT.NS', 'RATEGAIN.NS', 'RATNAVEER.NS', 'RAYMONDLSL.NS', 'RBA.NS', 'RBZJEWEL.NS', 'REDTAPE.NS', 'RELCHEMQ.NS', 'RELTD.NS', 'RETAIL.NS', 'REVATHIEQU.NS', 'RHL.NS', 'RISHABH.NS', 'RITCO.NS', 'RKSWAMY.NS', 'ROLEXRINGS.NS', 'ROSSARI.NS', 'ROTO.NS', 'ROUTE.NS', 'RPEL.NS', 'RPTECH.NS', 'RRKABEL.NS', 'RUBFILA.NS', 'RUSTOMJEE.NS', 'RVHL.NS', 'S&SPOWER.NS', 'SADHNANIQ.NS', 'SAH.NS', 'SAHYADRI.NS', 'SAMHI.NS', 'SANDUMA.NS', 'SANOFICONR.NS', 'SANSERA.NS', 'SANSTAR.NS', 'SAPPHIRE.NS', 'SATINDLTD.NS', 'SAURASHCEM.NS', 'SBC.NS', 'SBCL.NS', 'SBFC.NS', 'SBGLP.NS', 'SBICARD.NS', 'SCILAL.NS', 'SCPL.NS', 'SECMARK.NS', 'SENCO.NS', 'SGIL.NS', 'SHAH.NS', 'SHAILY.NS', 'SHAREINDIA.NS', 'SHIVALIK.NS', 'SHRIRAMPPS.NS', 'SHYAMMETL.NS', 'SIGACHI.NS', 'SIGMA.NS', 'SIGNATURE.NS', 'SIGNPOST.NS', 'SINCLAIR.NS', 'SINDHUTRAD.NS', 'SJS.NS', 'SKYGOLD.NS', 'SMCGLOBAL.NS', 'SMLT.NS', 'SONACOMS.NS', 'SPORTKING.NS', 'SRD.NS', 'SRGHFL.NS', 'SRM.NS', 'SSDL.NS', 'STANLEY.NS', 'STARHEALTH.NS', 'STARTECK.NS', 'STEELCAS.NS', 'STOVEKRAFT.NS', 'STYLAMIND.NS', 'STYLEBAAZA.NS', 'SUKHJITS.NS', 'SULA.NS', 'SUMICHEM.NS', 'SUNCLAY.NS', 'SUPRIYA.NS', 'SURAJEST.NS', 'SURAJLTD.NS', 'SURYODAY.NS', 'SUVENPHAR.NS', 'SUVIDHAA.NS', 'SUYOG.NS', 'SVPGLOB.NS', 'SYNCOMF.NS', 'SYRMA.NS', 'TARC.NS', 'TARIL.NS', 'TARSONS.NS', 'TATATECH.NS', 'TATVA.NS', 'TBOTEK.NS', 'TECILCHEM.NS', 'TEGA.NS', 'TIPSFILMS.NS', 'TMB.NS', 'TOLINS.NS', 'TRACXN.NS', 'TREL.NS', 'TRU.NS', 'TVSSCS.NS', 'UCAL.NS', 'UDAICEMENT.NS', 'UDS.NS', 'UGROCAP.NS', 'UJJIVANSFB.NS', 'UMAEXPORTS.NS', 'UNIDT.NS', 'UNIECOM.NS', 'UNIPARTS.NS', 'UNITDSPR.NS', 'UNIVPHOTO.NS', 'USK.NS', 'UTIAMC.NS', 'UTKARSHBNK.NS', 'UYFINCORP.NS', 'VALIANTLAB.NS', 'VALIANTORG.NS', 'VCL.NS', 'VENUSPIPES.NS', 'VERANDA.NS', 'VIJAYA.NS', 'VINEETLAB.NS', 'VIRINCHI.NS', 'VLEGOV.NS', 'VPRPL.NS', 'VRAJ.NS', 'VSTL.NS', 'WCIL.NS', 'WINDLAS.NS', 'XTGLOBAL.NS', 'YASHO.NS', 'YATHARTH.NS', 'YATRA.NS', 'YUKEN.NS', 'ZAGGLE.NS', 'ZIMLAB.NS', 'ZOMATO.NS']
