from litex.soc.cores import uart
from litex.soc.cores.uart import UARTWishboneBridge

from litex_boards.platforms import arty
from litex_boards.targets.arty import BaseSoC
from litex.soc.integration.builder import Builder

class BridgeSoC(BaseSoC):
    
    def __init__(self, platform, *args, **kwargs):
        sys_clk_freq = int(100e6)
        BaseSoC.__init__(self,sys_clk_freq,
            cpu_type=None,
            csr_data_width=32,
            with_uart=True,
            with_timer=False,
            uart_name="crossover"
        )
        self.bridge = UARTWishboneBridge(platform.request("serial"), self.clk_freq, baudrate=115200)
        self.add_wb_master(self.bridge.wishbone)

platform = arty.Platform()

soc = BridgeSoC(platform)
builder = Builder(soc,
                      output_dir="build", csr_csv="build/csr.csv",
                      compile_software=False)
vns = builder.build()
