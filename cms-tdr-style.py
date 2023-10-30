###
### CMS TDR STYLE 
###

import ROOT as rt
from array import array
rt.gROOT.SetBatch(rt.kTRUE)

cms_lumi = 'Run 2, 138 fb^{#minus1}'
cms_energy = '13'

cmsText     = 'CMS'
extraText   = 'Preliminary'

writeExtraText = True

cmsTextFont    = 61  #default is helvetic-bold
extraTextFont  = 52  #default is helvetica-italics
additionalInfoFont = 42
additionalInfo = [] # For extra info

# text sizes and text offsets with respect to the top frame in unit of the top margin size
lumiTextSize     = 0.6
lumiTextOffset   = 0.2
cmsTextSize      = 0.75
cmsTextOffset    = 0.1

# ratio of 'CMS' and extra text size
extraOverCmsTextSize  = 0.76

drawLogo     = False
kSquare      = True
kRectangular = False

# Define an alternative color palette and a function to set it
MyPalette = None


def SetEnergy(energy):
    global cms_energy
    cms_energy = str(energy)

def SetLumi(lumi, round_lumi=False):
    global cms_lumi
    if lumi!='':
        cms_lumi = f"{lumi:.0f}" if round_lumi else f"{lumi}"
        cms_lumi += " fb^{#minus1}"
    else:
        cms_lumi = lumi

def CreateAlternativePalette(alpha=1):
    red_values    = array('d', [0.00, 0.00, 1.00, 0.70])
    green_values  = array('d', [0.30, 0.50, 0.70, 0.00])
    blue_values   = array('d', [0.50, 0.40, 0.20, 0.15])
    length_values = array('d', [0.00, 0.15, 0.70, 1.00])
    num_colors = 200
    color_table = rt.TColor.CreateGradientColorTable(len(length_values), length_values, red_values, green_values, blue_values, num_colors,alpha)
    global MyPalette
    MyPalette = [color_table + i for i in range(num_colors)]

def SetAlternative2DColor(hist=None, style=None, alpha=1):
    global MyPalette
    if MyPalette is None:
        CreateAlternativePalette(alpha=alpha)
    if style is None:
        global tdrStyle
        style = tdrStyle
    style.SetPalette(len(MyPalette), array('i', MyPalette))
    if hist is not None:
        hist.SetContour(len(MyPalette))

def GetPalette(hist):
    ''' Allow to retrieve palette option. Must update the pad to access the palette '''
    UpdatePad()
    palette = hist.GetListOfFunctions().FindObject("palette")
    return palette

def UpdatePalettePosition(hist, canv=None, X1=None, X2=None, Y1=None, Y2=None, isNDC=True):
    ''' Adjust palette position '''
    palette = GetPalette(hist)
    if canv != None:
        hframe = GettdrCanvasHist(canv)
        X1 = 1 - canv.GetRightMargin()*0.95
        X2 = 1 - canv.GetRightMargin()*0.70
        Y1 = canv.GetBottomMargin()
        Y2 = 1 - canv.GetTopMargin()
    if isNDC:
        if X1 != None: palette.SetX1NDC(X1)
        if X2 != None: palette.SetX2NDC(X2)
        if Y1 != None: palette.SetY1NDC(Y1)
        if Y2 != None: palette.SetY2NDC(Y2)
    else:
        if X1 != None: palette.SetX1(X1)
        if X2 != None: palette.SetX2(X2)
        if Y1 != None: palette.SetY1(Y1)
        if Y2 != None: palette.SetY2(Y2)

# ######## ########  ########        ######  ######## ##    ## ##       ########
#    ##    ##     ## ##     ##      ##    ##    ##     ##  ##  ##       ##
#    ##    ##     ## ##     ##      ##          ##      ####   ##       ##
#    ##    ##     ## ########        ######     ##       ##    ##       ######
#    ##    ##     ## ##   ##              ##    ##       ##    ##       ##
#    ##    ##     ## ##    ##       ##    ##    ##       ##    ##       ##
#    ##    ########  ##     ##       ######     ##       ##    ######## ########

tdrStyle = None

# Turns the grid lines on (true) or off (false)
def tdrGrid(gridOn):
    tdrStyle.SetPadGridX(gridOn)
    tdrStyle.SetPadGridY(gridOn)

# Redraws the axis
def fixOverlay():
    rt.gPad.RedrawAxis()

def UpdatePad(pad=None):
    if pad:
        pad.Modified()
        pad.Update()
    else:
        rt.gPad.Modified()
        rt.gPad.Update()

def setTDRStyle():
    global tdrStyle
    if tdrStyle!=None:
        del tdrStyle
    tdrStyle = rt.TStyle('tdrStyle', 'Style for P-TDR')
    rt.gROOT.SetStyle(tdrStyle.GetName())
    rt.gROOT.ForceStyle()
    #for the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(rt.kWhite)
    tdrStyle.SetCanvasDefH(600) #Height of canvas
    tdrStyle.SetCanvasDefW(600) #Width of canvas
    tdrStyle.SetCanvasDefX(0)   #Position on screen
    tdrStyle.SetCanvasDefY(0)
    tdrStyle.SetPadBorderMode(0)
    tdrStyle.SetPadColor(rt.kWhite)
    tdrStyle.SetPadGridX(False)
    tdrStyle.SetPadGridY(False)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)
    #For the frame:
    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)
    #For the histo:
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(1)
    tdrStyle.SetEndErrorSize(2)
    tdrStyle.SetMarkerStyle(20)
    #For the fit/function:
    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat('5.4g')
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)
    #For the date:
    tdrStyle.SetOptDate(0)
    #For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat('mr')
    tdrStyle.SetStatColor(rt.kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat('6.4g')
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)
    # Margins:
    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.13)
    tdrStyle.SetPadLeftMargin(0.16)
    tdrStyle.SetPadRightMargin(0.02)
    # For the Global title:
    tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)
    # For the axis titles:
    tdrStyle.SetTitleColor(1, 'XYZ')
    tdrStyle.SetTitleFont(42, 'XYZ')
    tdrStyle.SetTitleSize(0.06, 'XYZ')
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.25)
    # For the axis labels:
    tdrStyle.SetLabelColor(1, 'XYZ')
    tdrStyle.SetLabelFont(42, 'XYZ')
    tdrStyle.SetLabelOffset(0.012, 'XYZ')
    tdrStyle.SetLabelSize(0.05, 'XYZ')
    # For the axis:
    tdrStyle.SetAxisColor(1, 'XYZ')
    tdrStyle.SetStripDecimals(True)
    tdrStyle.SetTickLength(0.03, 'XYZ')
    tdrStyle.SetNdivisions(510, 'XYZ')
    tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickY(1)
    # Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)
    # Postscript options:
    tdrStyle.SetPaperSize(20.,20.)
    tdrStyle.SetHatchesLineWidth(5)
    tdrStyle.SetHatchesSpacing(0.05)
    tdrStyle.cd()


#  ######  ##     ##  ######       ##       ##     ## ##     ## ####
# ##    ## ###   ### ##    ##      ##       ##     ## ###   ###  ##
# ##       #### #### ##            ##       ##     ## #### ####  ##
# ##       ## ### ##  ######       ##       ##     ## ## ### ##  ##
# ##       ##     ##       ##      ##       ##     ## ##     ##  ##
# ##    ## ##     ## ##    ##      ##       ##     ## ##     ##  ##
#  ######  ##     ##  ######       ########  #######  ##     ## ####


def CMS_lumi(pad, iPosX=11, scaleLumi=None):
    relPosX    = 0.035
    relPosY    = 0.035
    relExtraDY = 1.2
    outOfFrame = int(iPosX / 10) == 0
    alignX_ = max(int(iPosX / 10), 1)
    alignY_ = 1 if iPosX == 0 else 3
    align_ = 10*alignX_ + alignY_
    H = pad.GetWh()*pad.GetHNDC()
    W = pad.GetWw()*pad.GetWNDC()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    outOfFrame_posY = 1-t+lumiTextOffset*t
    pad.cd()
    lumiText = ''
    lumiText += cms_lumi
    if cms_energy!='':
        lumiText += ' ('+cms_energy+' TeV)'
    if scaleLumi:
        lumiText = ScaleText(lumiText, scale = scaleLumi)
    
    def drawText(text, posX, posY, font, align, size):
        latex.SetTextFont(font)
        latex.SetTextAlign(align)
        latex.SetTextSize(size)
        latex.DrawLatex(posX, posY,text)

    latex = rt.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(rt.kBlack)
    extraTextSize = extraOverCmsTextSize*cmsTextSize
    drawText(text=lumiText, posX=1-r, posY=outOfFrame_posY, font=42, align=31, size=lumiTextSize*t)
    if outOfFrame:
        drawText(text=cmsText, posX=l, posY=outOfFrame_posY, font=cmsTextFont, align=11, size=cmsTextSize*t)
    posX_ = 0
    if (iPosX%10<=1):
        posX_ = l + relPosX*(1-l-r)
    elif (iPosX%10==2):
        posX_ = l + 0.5*(1-l-r)
    elif (iPosX%10==3):
        posX_ = 1 - r - relPosX*(1-l-r)
    posY_ = 1 - t - relPosY*(1-t-b)
    if not outOfFrame:
        if drawLogo:
            posX_ =   l + 0.045*(1-l-r)*W/H
            posY_ = 1-t - 0.045*(1-t-b)
            xl_0 = posX_
            yl_0 = posY_ - 0.15
            xl_1 = posX_ + 0.15*H/W
            yl_1 = posY_
            CMS_logo = rt.TASImage('CMS-BW-label.png')
            pad_logo =  rt.TPad('logo','logo', xl_0, yl_0, xl_1, yl_1)
            pad_logo.Draw()
            pad_logo.cd()
            CMS_logo.Draw('X')
            pad_logo.Modified()
            pad.cd()
        else:
            drawText(text=cmsText, posX=posX_, posY=posY_, font=cmsTextFont, align=align_, size=cmsTextSize*t)
            if writeExtraText:
                posY_ -= relExtraDY*cmsTextSize*t
                drawText(text=extraText, posX=posX_, posY=posY_, font=extraTextFont, align=align_, size=extraTextSize*t)
                if (len(additionalInfo)!=0):
                    latex.SetTextSize(extraTextSize*t)
                    latex.SetTextFont(additionalInfoFont)
                    for ind,tt in enumerate(additionalInfo):
                        latex.DrawLatex(posX_, posY_ - 0.004 -(relExtraDY*extraTextSize*t/2 + 0.02)*(ind+1), tt)
    elif writeExtraText:
        if (outOfFrame):
            scale = float(H)/W if W>H else 1
            posX_ = l + 0.043*(extraTextFont*t*cmsTextSize)*scale
            posY_ = outOfFrame_posY
        drawText(text=extraText, posX=posX_, posY=posY_, font=extraTextFont, align=align_, size=extraTextSize*t)
    UpdatePad(pad)



# ########  ##        #######  ######## ######## #### ##    ##  ######         ##     ##    ###     ######  ########   #######   ######
# ##     ## ##       ##     ##    ##       ##     ##  ###   ## ##    ##        ###   ###   ## ##   ##    ## ##     ## ##     ## ##    ##
# ##     ## ##       ##     ##    ##       ##     ##  ####  ## ##              #### ####  ##   ##  ##       ##     ## ##     ## ##
# ########  ##       ##     ##    ##       ##     ##  ## ## ## ##   ####       ## ### ## ##     ## ##       ########  ##     ##  ######
# ##        ##       ##     ##    ##       ##     ##  ##  #### ##    ##        ##     ## ######### ##       ##   ##   ##     ##       ##
# ##        ##       ##     ##    ##       ##     ##  ##   ### ##    ##        ##     ## ##     ## ##    ## ##    ##  ##     ## ##    ##
# ##        ########  #######     ##       ##    #### ##    ##  ######         ##     ## ##     ##  ######  ##     ##  #######   ######


# Create canvas with predefined axix and CMS logo
def tdrCanvas(canvName, x_min, x_max, y_min, y_max, nameXaxis, nameYaxis, square=kSquare, iPos=11, extraSpace=0, with_z_axis=False, scaleLumi=None):
    """
    Draw a canvas with TDR style.
    
    canvName: Name of the canvas.
    x_min: Minimum value of the x-axis.
    x_max: Maximum value of the x-axis.
    y_min: Minimum value of the y-axis.
    y_max: Maximum value of the y-axis.
    nameXaxis: Label for the x-axis.
    nameYaxis: Label for the y-axis.
    square: If True, canvas is square.
    iPos: Position of the CMS logo in the plot.
        iPos=11 : top-left, left-aligned
        iPos=33 : top-right, right-aligned
        iPos=22 : center, centered
        iPos=0  : out of frame (in exceptional cases)
        mode generally : iPos = 10*(alignement 1/2/3) + position (1/2/3 = l/c/r)
    extraSpace: add extra space to the left margins to fit lable
    is2D: If True, canvas is 2D.
    """

    # Set TDR style
    setTDRStyle()

    # Set canvas dimensions and margins
    W_ref = 600 if square else 800
    H_ref = 600 if square else 600

    W = W_ref
    H = H_ref
    T = 0.07*H_ref
    B = 0.11*H_ref
    L = 0.13*H_ref
    R = 0.03*H_ref

    canv = rt.TCanvas(canvName,canvName,50,50,W,H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetLeftMargin(L/W+extraSpace)
    canv.SetRightMargin(R/W)
    if with_z_axis:
        canv.SetRightMargin(B/W+0.03)
    canv.SetTopMargin(T/H)
    canv.SetBottomMargin(B/H + 0.02)

    # Draw frame and set axis labels
    h = canv.DrawFrame(x_min, y_min, x_max, y_max)
    y_offset = 1.2 if square else 0.8
    h.GetYaxis().SetTitleOffset(y_offset)
    h.GetXaxis().SetTitleOffset(0.9)
    h.GetXaxis().SetTitle(nameXaxis)
    h.GetYaxis().SetTitle(nameYaxis)
    h.Draw('AXIS')

    # Draw CMS logo and update canvas
    CMS_lumi(canv, iPos, scaleLumi=scaleLumi)
    UpdatePad(canv)
    canv.RedrawAxis()
    canv.GetFrame().Draw()
    return canv

def GettdrCanvasHist(canv):
    return canv.GetListOfPrimitives().FindObject('hframe')

def tdrCanvasResetAxes(canv, x_min, x_max, y_min, y_max):
    GettdrCanvasHist(canv).GetXaxis().SetRangeUser(x_min,x_max)
    GettdrCanvasHist(canv).GetYaxis().SetRangeUser(y_min,y_max)

def tdrDiCanvas(canvName, x_min, x_max, y_min, y_max, r_min, r_max, nameXaxis, nameYaxis, nameRatio, square=kSquare, iPos=11, extraSpace=0, scaleLumi=None):
    setTDRStyle()

    W_ref = 700 if square else 800
    H_ref = 600 if square else 500
    # Set bottom pad relative height and relative margin
    F_ref = 1./3.
    M_ref = 0.03
    # Set reference margins
    T_ref = 0.07
    B_ref = 0.13
    L = 0.15 if square else 0.12
    R = 0.05
    # Calculate total canvas size and pad heights
    W = W_ref
    H = int(H_ref * (1 + (1-T_ref-B_ref)*F_ref+M_ref))
    Hup = H_ref * (1-B_ref)
    Hdw = H - Hup
    # references for T, B, L, R
    Tup = T_ref * H_ref / Hup
    Tdw = M_ref * H_ref / Hdw
    Bup = 0.022
    Bdw = B_ref * H_ref / Hdw

    canv = rt.TCanvas(canvName,canvName,50,50,W,H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetFrameLineColor(0)
    canv.SetFrameLineWidth(0)
    canv.Divide(1,2)

    canv.cd(1)
    rt.gPad.SetPad(0, Hdw / H, 1, 1)
    rt.gPad.SetLeftMargin(L)
    rt.gPad.SetRightMargin(R)
    rt.gPad.SetTopMargin(Tup)
    rt.gPad.SetBottomMargin(Bup)

    hup = canv.cd(1).DrawFrame(x_min,y_min,x_max,y_max)
    hup.GetYaxis().SetTitleOffset(extraSpace+(1.1 if square else 0.9)* Hup / H_ref)
    hup.GetXaxis().SetTitleOffset(999)
    hup.GetXaxis().SetLabelOffset(999)
    hup.SetTitleSize(hup.GetTitleSize('Y') * H_ref / Hup, 'Y')
    hup.SetLabelSize(hup.GetLabelSize('Y') * H_ref / Hup, 'Y')
    hup.GetYaxis().SetTitle(nameYaxis)

    CMS_lumi(rt.gPad, iPos, scaleLumi=scaleLumi)

    canv.cd(2)
    rt.gPad.SetPad(0, 0, 1, Hdw / H)
    rt.gPad.SetLeftMargin(L)
    rt.gPad.SetRightMargin(R)
    rt.gPad.SetTopMargin(Tdw)
    rt.gPad.SetBottomMargin(Bdw)

    hdw = canv.cd(2).DrawFrame(x_min,r_min,x_max,r_max)
    # Scale text sizes and margins to match normal size
    hdw.GetYaxis().SetTitleOffset(extraSpace+(1.0 if square else 0.8)* Hdw / H_ref)
    hdw.GetXaxis().SetTitleOffset(0.9)
    hdw.SetTitleSize(hdw.GetTitleSize('Y') * H_ref / Hdw, 'Y')
    hdw.SetLabelSize(hdw.GetLabelSize('Y') * H_ref / Hdw, 'Y')
    hdw.SetTitleSize(hdw.GetTitleSize('X') * H_ref / Hdw, 'X')
    hdw.SetLabelSize(hdw.GetLabelSize('X') * H_ref / Hdw, 'X')
    hdw.SetLabelOffset(hdw.GetLabelOffset('X')*H_ref / Hdw, 'X')
    hdw.GetXaxis().SetTitle(nameXaxis)
    hdw.GetYaxis().SetTitle(nameRatio)

    # Set tick lengths to match original (these are fractions of axis length)
    hdw.SetTickLength(hdw.GetTickLength('Y') * H_ref / Hup, 'Y') #?? ok if 1/3
    hdw.SetTickLength(hdw.GetTickLength('X') * H_ref / Hdw, 'X')

    # Reduce divisions to match smaller height (default n=510, optim=kTRUE)
    hdw.GetYaxis().SetNdivisions(505)
    hdw.Draw('AXIS')
    canv.cd(1)
    UpdatePad(canv.cd(1))
    canv.cd(1).RedrawAxis()
    canv.cd(1).GetFrame().Draw()
    return canv

def tdrLeg(x1, y1, x2, y2, textSize=0.04, textFont=42, textColor=rt.kBlack, columns=None):
    leg = rt.TLegend(x1, y1, x2, y2, '', 'brNDC')
    leg.SetTextSize(textSize)
    leg.SetTextFont(textFont)
    leg.SetTextColor(textColor)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    if columns:
        leg.SetNColumns(columns)
    leg.Draw()
    return leg

#To be fixed as python deletes obj before time
def tdrHeader(leg, legTitle, textAlign=12, textSize=0.04, textFont=42, textColor=rt.kBlack, isToRemove=True):
    header = rt.TLegendEntry(0, legTitle, "h")
    header.SetTextFont(textFont)
    header.SetTextSize(textSize)
    header.SetTextAlign(textAlign)
    header.SetTextColor(textColor)
    if isToRemove:
        leg.SetHeader(legTitle,'C')
        leg.GetListOfPrimitives().Remove(leg.GetListOfPrimitives().At(0))
        leg.GetListOfPrimitives().AddAt(header,0)
    else:
        leg.GetListOfPrimitives().AddLast(header)


# ########  ########     ###    ##      ##
# ##     ## ##     ##   ## ##   ##  ##  ##
# ##     ## ##     ##  ##   ##  ##  ##  ##
# ##     ## ########  ##     ## ##  ##  ##
# ##     ## ##   ##   ######### ##  ##  ##
# ##     ## ##    ##  ##     ## ##  ##  ##
# ########  ##     ## ##     ##  ###  ###

def tdrDraw(h, style, marker=rt.kFullCircle, msize=1.0, mcolor=rt.kBlack, lstyle=rt.kSolid, lwidth=1, lcolor=-1, fstyle=1001, fcolor=rt.kYellow+1, alpha=-1):
    h.SetMarkerStyle(marker)
    h.SetMarkerSize(msize)
    h.SetMarkerColor(mcolor)
    h.SetLineStyle(lstyle)
    h.SetLineWidth(lwidth)
    h.SetLineColor(mcolor if lcolor==-1 else lcolor)
    h.SetFillStyle(fstyle)
    h.SetFillColor(fcolor)
    if alpha>0: h.SetFillColorAlpha(fcolor, alpha)
    h.Draw(style+'SAME')

def tdrDrawLine(line, lcolor=rt.kRed, lstyle=rt.kSolid, lwidth=2):
    line.SetLineStyle(lstyle)
    line.SetLineColor(lcolor)
    line.SetLineWidth(lwidth)
    line.Draw('SAME')

def ScaleText(name, scale = 0.75):
    return '#scale['+str(scale)+']{'+str(name)+'}'

def SaveCanvas(canv, path, close=True):
    ''' Takes care of fixing overlay and closing object '''
    fixOverlay()
    canv.SaveAs(path)
    if close:
        canv.Close()
