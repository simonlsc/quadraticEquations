from doctest import run_docstring_examples
from re import A
from manim import *
import math

from numpy import Inf

class graphPaper(Scene):
    def __init__(self):
        super().__init__()
        # self.axes = Axes(
        #     x_range=[-8, 8, 1],
        #     y_range=[-5, 5, 1],
        #     x_length=16,
        #     axis_config={"color": GREEN},
        #     x_axis_config={
        #         "numbers_to_include": np.arange(-8, 8, 1),
        #         "numbers_with_elongated_ticks": np.arange(-8, 8, 1),
        #     },
        #     y_axis_config={
        #         "numbers_to_include": np.arange(-5, 5, 1),
        #         "numbers_with_elongated_ticks": np.arange(-5, 5, 1),
        #     },            
        #     tips=False,
        # )
        self.axes=Axes()
        def get_grid(sx, ex, dx, sy, ey, dy):
            def get_line(s,e):
                return Line(s,e,color=GREY, stroke_width=1)

            ctp = self.axes.coords_to_point
            v_lines = VGroup(*[get_line(ctp(x,sy), ctp(x,ey)) for x in np.arange(sx,ex+dx,dx)])
            h_lines = VGroup(*[get_line(ctp(sx,y), ctp(ex,y)) for y in np.arange(sy,ey+dy,dy)])

            return VGroup(v_lines, h_lines)
        # SET INITIAL STATE OF GRAPH

        grid = get_grid(*self.axes.x_range, *self.axes.y_range)
        self.add(self.axes)
        self.add(grid)



class StaightLinePassThroughOrigin(graphPaper):
    def construct(self):
        # SETUP GRAPH
        mStart=1
        mMax=7.5
        mMin=-mMax
        mMid=(mMax+mMin)/2
        cStart=0
        cMax=3
        cMin=-cMax
        func = lambda m,c: lambda x: m * x + c
        graph = VMobject()
        graph_kwargs = {"color": GREEN}
        # SETUP FORMULA
        slope = DecimalNumber(mStart,num_decimal_places=2,include_sign=True,color=YELLOW)
        intercept = DecimalNumber(cStart,num_decimal_places=2,include_sign=True,color=PURE_RED)
        formula = MathTex("y = ", "9.99","x","-9.99")
        # ---- Arrange position of formula
        formula.to_corner(UR)
        formula[0].shift(LEFT*0.5)

        slope.add_updater(lambda d: d.next_to(formula[0],RIGHT,aligned_edge=DOWN))
        intercept.add_updater(lambda d: d.next_to(formula[2],RIGHT,aligned_edge=DOWN))


        # SET UPDATERS
        def update_graph(mob):
            mob.become(
                self.axes.plot(
                    func(slope.get_value(),intercept.get_value()),
                    **graph_kwargs
                )
            )
        # SET INITIAL STATE OF GRAPH
        update_graph(graph)
        graph.add_updater(update_graph)
        self.play(Create(graph),Write(VGroup(formula[0],slope,formula[2],intercept)))

        for mExtreme in [mMax,mMid,mMin,-1]:
            self.play(
                ChangeDecimalToValue(slope,mExtreme),
                run_time=5,
            )
            self.wait()

        for cExtreme in [cMax,cMin,cStart]:
            self.play(
                ChangeDecimalToValue(intercept,cExtreme),
                run_time=5,
            )
            self.wait()




class mXsquareMinusC(graphPaper):
    def construct(self):
        # SETUP GRAPH
        func = lambda m, c: lambda x: m * x * x + c
        graph = VMobject()
        graph_kwargs = {"color": GREEN}
        # SETUP FORMULA
        c2 = DecimalNumber(1,num_decimal_places=2,include_sign=True,color=YELLOW)
        c0 = DecimalNumber(-4,num_decimal_places=2,include_sign=True,color=LIGHT_PINK)
        formula = MathTex("y = ", "+9.99"," x^2","-9.99")
        # ---- Arrange position of formula
        formula.to_corner(UR)
        formula[0].shift(LEFT * 0.5)

        c2.add_updater(lambda d: d.next_to(formula[0],RIGHT))
        c0.add_updater(lambda d: d.next_to(formula[2],RIGHT))

        # SET UPDATERS
        def update_graph(mob):
            mob.become(
                self.axes.plot(
                    func(c2.get_value(),c0.get_value()),
                    **graph_kwargs
                )
            )
        # SET INITIAL STATE OF GRAPH
        update_graph(graph)
        graph.add_updater(update_graph)
        self.play(Create(graph),Write(VGroup(formula[0],c2,formula[2],c0)))
        self.wait(2)
        for m in [4,0,-4,-1]:
            self.play(
                ChangeDecimalToValue(c2,m),
                run_time=3
            )
            self.wait()

        for c in [0,4,0]:
            self.play(
                ChangeDecimalToValue(c0,c),
                run_time=3
            )
            self.wait()

        for m in [0,1]:
            self.play(
                ChangeDecimalToValue(c2,m),
                run_time=3
            )
            self.wait()

        for c in [-4]:
            self.play(
                ChangeDecimalToValue(c0,c),
                run_time=3
            )
            self.wait()


class movingRoots(graphPaper):
    def __init__(self):
        super().__init__()    

    def construct(self):
        # SETUP GRAPH
        func = lambda a, b: lambda x: (x + a) * (x + b)
        graph = VMobject()
        graph_kwargs = {"color": GREEN}
        # SETUP FORMULA
        alpha = DecimalNumber(2,num_decimal_places=2,include_sign=True,color=YELLOW)
        beta = DecimalNumber(-2,num_decimal_places=2,include_sign=True,color=PURE_BLUE)
        formula = MathTex("y = (x", "+9.99",")(x","-9.99,",")")
        sumOfRoot = DecimalNumber(alpha.get_value()+beta.get_value(),num_decimal_places=2,include_sign=True,color=PURE_RED)
        productOfRoot = DecimalNumber(alpha.get_value()*beta.get_value(),num_decimal_places=2,include_sign=True,color=PURE_GREEN)

        expand = MathTex("y = x^2", "+99.99","x","-99.99")

#        alpha.add_updater(lambda d: d.set_value(alpha_tracker.get_value()+beta_tracker.get_value()))
        alpha.add_updater(lambda d: d.next_to(formula[0],RIGHT))
        beta.add_updater(lambda d: d.next_to(formula[2],RIGHT))


        sumOfRoot.add_updater(lambda d: d.set_value(alpha.get_value()+beta.get_value()))
        sumOfRoot.add_updater(lambda d: d.next_to(expand[0],RIGHT))
        productOfRoot.add_updater(lambda d: d.set_value(alpha.get_value()*beta.get_value()))
        productOfRoot.add_updater(lambda d: d.next_to(expand[2],RIGHT))
        # ---- Arrange position of formula
        formula.to_corner(UR)
        formula[0].shift(LEFT * 0.5)

        expand.to_corner(UL)

        alpha.next_to(formula[0],RIGHT,aligned_edge=DOWN)
        beta.next_to(formula[2],RIGHT,aligned_edge=DOWN)
        # SET UPDATERS
        def update_graph(mob):
            mob.become(
                self.axes.plot(
                    func(alpha.get_value(),beta.get_value()),
                    **graph_kwargs
                )
            )

        update_graph(graph)
        graph.add_updater(update_graph)
        self.play(Create(graph),
                    Write(VGroup(formula[0],alpha,formula[2],beta,formula[4])),
                    Write(VGroup(expand[0],sumOfRoot,expand[2],productOfRoot))                    
                )
        self.wait(2)

        for a,b in [[0,-4],[-1,-4],[1,-3],[6,1],[2,-2]]:
            self.play(
                ChangeDecimalToValue(alpha,a),            
                ChangeDecimalToValue(beta,b),
                run_time=3
            )
            self.wait(2)



class higherDegrees(Scene):
    def __init__(self):
        super().__init__()    

    def construct(self):
        axes=Axes(y_range=[-10,10,10])
        self.add(axes)               
        # SETUP GRAPH
        graph = VMobject()
        graph_kwargs = {"color": GREEN}
        # SETUP FORMULA
        funcList = [
                        lambda x: (x + 3) * (x - 3),
                        lambda x: (x + 3) * x * (x - 3) / 1.5,
                        lambda x: (x + 6) * (x + 3) * (x - 3) * (x - 6) / 40,
                        lambda x: (x + 6) * (x + 3) * x * (x - 3) * (x - 6) / 80,
                        lambda x: (x + 7) * (x + 5) * (x + 3) * (x - 3) * (x - 5) * (x - 7) / 900,
                        lambda x: (x + 7) * (x + 5) * (x + 3) * x * (x - 3) * (x - 5) * (x - 7) / 2000,
        ]
        formulaList = [
                        MathTex("y = (x+3)(x-3)"),
                        MathTex("y = (x+3)x(x-3)"),
                        MathTex("y = (x+6)(x+3)(x-3)(x-6)"),
                        MathTex("y = (x+6)(x+3)x(x-3)(x-6)"),
                        MathTex("y = (x+7)(x+5)(x+3)(x-3)(x-5)(x-7)"),
                        MathTex("y = (x+7)(x+5)(x+3)x(x-3)(x-5)(x-7)")
        ]

        def update_to_graph(i):
            graph.become(
                axes.plot(
                    funcList[i],
                    **graph_kwargs
                )
            )

        update_to_graph(0)

        formulaList[0].to_corner(UR)

        currentMathTex=formulaList[0]
        currentGraph=axes.plot(funcList[0],**graph_kwargs)

#        self.play(Create(graph),Write(currentMathTex))
#        self.wait(2)
        transitTime=4

        for i in range(len(funcList)):
            nextGraph=axes.plot(funcList[i],**graph_kwargs)
            self.play(ReplacementTransform(currentGraph,nextGraph),ReplacementTransform(currentMathTex,formulaList[i].to_corner(UR)),run_time=transitTime)
            currentMathTex=formulaList[i]
            currentGraph=nextGraph
            self.wait(transitTime)


