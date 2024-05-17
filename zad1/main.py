import click
import math
import matplotlib
import matplotlib.pyplot as plt

def camera_params() -> tuple:
    f = click.prompt("Podaj ogniskową kamery [mm]", type=float)
    while f <= 0:
        click.echo('Wartość f nie może być mniejsza lub równa 0')
        f = click.prompt("Podaj ogniskową kamery [mm]", type=float)
    f = f*10**-3
    px = click.prompt("Podaj px [μm]", type=float)
    while px <= 0:
        click.echo('Wartość px nie może być mniejsza lub równa 0')
        px = click.prompt("Podaj px [μm]", type=float)
    px = px*10**-6
    lX = click.prompt("Podaj lX [m]", type=float)
    while lX <= 0:
        click.echo('Wartość lX nie może być mniejsza lub równa 0')
        lX = click.prompt("Podaj lX [m]", type=float)
    lY = click.prompt("Podaj lY [m]", type=float)
    while lY <= 0:
        click.echo('Wartość lY nie może być mniejsza lub równa 0')
        lY = click.prompt("Podaj lY [m]", type=float)
    cycle = click.prompt("Podaj cykl pracy kamery [s]", type=float)
    while cycle <= 0:
        click.echo('Wartość cyklu pracy kamery nie może być mniejsza lub równa 0')
        cycle = click.prompt("Podaj cykl pracy kamery [s]", type=float)
    return f, px, lX, lY, cycle

def calc_and_print_params(lX, lY, p, q, DX, DY, gsd, cycle, speed) -> tuple:
    Lx = lX * gsd
    Ly = lY * gsd
    Bx = Lx * (1 - p)
    By = Ly * (1 - q)
    Pz = Lx * Ly
    Pm = (Lx - Bx) * Ly
    Pn = Bx * By
    Ny = DX / Bx
    Nx = DY / By + 2
    Ny = math.ceil(Ny)
    Nx = math.ceil(Nx)
    click.echo(f"Wartości dla podanego GSD = {gsd}m:")
    click.echo(f"Lx: {round(Lx)}m")
    click.echo(f"Ly: {round(Ly)}m")
    click.echo(f"Bx: {round(Bx)}m")
    click.echo(f"By: {round(By)}m")
    click.echo(f"Pz: {round(Pz)}m2")
    click.echo(f"Pm: {round(Pm)}m2")
    click.echo(f"Pn: {round(Pn)}m2")
    click.echo(f"Ny: {Ny}")
    click.echo(f"Nx: {Nx}")
    bx_speed = Bx / speed
    if bx_speed < cycle:
        click.echo(f"Minimalna prędkość pokonania jednego Bx wynosi {round(bx_speed, 2)}m/s, a cykl pracy kamery wynosi {cycle}s")
    return Lx, Ly, Bx, By, Pz, Pm, Pn, Ny, Nx

@click.command()
def main():
    Hsr = click.prompt("Podaj średnią wysokość terenu na obszarze opracowania [m]", type=float)
    while Hsr <= 0:
        click.echo('Wartość średniej wysokości terenu nie może być mniejsza lub równa 0')
        Hsr = click.prompt("Podaj średnią wysokość terenu na obszarze opracowania", type=float)
    click.echo("Wybrać domyślną kamerę spośród podanych czy podać parametry kamery?")
    click.echo("1. Podać parametry kamery")
    click.echo("2. Z/I DMC IIe 230")
    click.echo("3. Leica DMC III")
    click.echo("4. UltraCam Falcon M2 70")
    click.echo("5. UltraCam Eagle M2 80")
    choice = click.prompt("Wybierz opcję", type=int)
    match choice:
        case 1:
            f, px, lX, lY, cycle = camera_params()
        case 2:
            f, px, lX, lY, cycle = 92*10**-3, 5.6*10**-6, 15552, 14144, 1.8
        case 3:
            f, px, lX, lY, cycle = 92*10**-3, 3.9*10**-6, 25728, 14592, 1.9
        case 4:
            f, px, lX, lY, cycle = 70*10**-3, 6.0*10**-6, 17310, 11310, 1.35
        case 5:
            f, px, lX, lY, cycle = 80*10**-3, 4.6*10**-6, 23010, 14790, 1.65
        case _:
            click.echo("Podano nieprawidłową wartość, podaj parametry kamery")
            f, px, lX, lY, cycle = camera_params()
    gsd = click.prompt("Podaj GSD [m]", type=float)
    while gsd <= 0:
        click.echo('Wartość GSD nie może być mniejsza lub równa 0')
        gsd = click.prompt("Podaj GSD [m]", type=float)
    click.echo(f"Podaj Xmin, Xmax, Ymin, Ymax")
    Xmin = click.prompt("Xmin [m]", type=float)
    Xmax = click.prompt("Xmax [m]", type=float)
    while Xmax <= Xmin:
        click.echo('Wartość Xmax nie może być mniejsza lub równa Xmin')
        Xmax = click.prompt("Xmax [m]", type=float)
    Ymin = click.prompt("Ymin [m]", type=float)
    Ymax = click.prompt("Ymax [m]", type=float)
    while Ymax <= Ymin:
        click.echo('Wartość Ymax nie może być mniejsza lub równa Ymin')
        Ymax = click.prompt("Ymax [m]", type=float)
    Xmin, Xmax, Ymin, Ymax = Ymin, Ymax, Xmin, Xmax # geodesy moment
    DX = Xmax - Xmin
    DY = Ymax - Ymin
    p = click.prompt("Podaj p [część dziesiętna]", type=float)
    while p <= 0 or p >= 1:
        click.echo('Wartość p musi być większa niż 0 i mniejsza niż 1')
        p = click.prompt("Podaj p [część dziesiętna]", type=float)
    q = click.prompt("Podaj q [część dziesiętna]", type=float)
    while q <= 0 or q >= 1:
        click.echo('Wartość q musi być większa niż 0 i mniejsza niż 1')
        q = click.prompt("Podaj q [część dziesiętna]", type=float)
    Wmax = gsd * f / px + Hsr
    if Wmax <= Hsr:
        click.echo(f"Coś poszło nie tak, wysokość lotu musi być większa niż {round(Wmax)}m, podana średnia wysokość podanego terenu to {round(Hsr)}m")
        return
    click.echo(f"Wysokość lotu musi być większa niż {round(Wmax)}m, podana średnia wysokość podanego terenu to {round(Hsr)}m")
    click.echo(f"Dostępne samoloty na danym pułapie to:")
    planes = [['Tencam MMA', 4572, 120], ['Cessna T206H NAV III', 4785, 100], ['Vulcan Air P68 Obeserver 2', 6100, 135], ['Cessna 402', 8200, 132]]
    for plane in planes:
        plane_gsd = (plane[1]-Hsr) * px / f
        if Wmax <= plane[1]:
            click.echo(f"{plane[0]} z maksymalnym pułapem {plane[1]}m i maksymalnym GSD równym {round(plane_gsd,2)}m")
        else:
            click.echo(f"Potrzebna wysokość lotu dla samolotu {plane[0]} jest zbyt duża, maksymalny pułap lotu samolotu wynosi {plane[1]}m, a maksymalne GSD dla tego samolotu to {round(plane_gsd,2)}m")
    s = 0
    W = 0
    available_planes = [p for p in planes if Wmax <= p[1]]
    click.echo("Wybierz samolot z listy lub podaj własną wysokość lotu")
    click.echo("1. Podaj własną wysokość lotu")
    for i, plane in enumerate(available_planes):
        if Wmax <= plane[1]:
            click.echo(f"{i+2}. {plane[0]}")
    plane_choice = click.prompt("Wybierz samolot", type=int)
    while plane_choice not in range(1, len(available_planes)+2):
        click.echo("Podano nieprawidłową wartość")
        plane_choice = click.prompt("Wybierz samolot", type=int)
    if plane_choice == 1:
        W = click.prompt("Podaj wysokość lotu [m]", type=float)
        while W <= Wmax:
            click.echo(f"Wysokość lotu musi być większa niż {round(Wmax)}m")
            W = click.prompt("Podaj wysokość lotu [m]", type=float)
        s = click.prompt("Podaj prędkość lotu [m/s]", type=float)
        while s <= 0:
            click.echo('Wartość prędkości lotu nie może być mniejsza lub równa 0')
            s = click.prompt("Podaj prędkość lotu [m/s]", type=float)
    else:
        W = planes[plane_choice-2][1]
        s = planes[plane_choice-2][2]

    Lx, Ly, Bx, By, _, _, _, Ny, Nx = calc_and_print_params(lX, lY, p, q, DX, DY, gsd, cycle, s)
    powtorzyc = 'tak'
    while powtorzyc == 'tak':
        click.echo("Czy chcesz powtórzyć obliczenia dla innej wartości GSD?")
        powtorzyc = click.prompt("Tak/Nie", type=str)
        powtorzyc = powtorzyc.lower()

        while powtorzyc not in ['tak', 'nie']:
            click.echo("Podano nieprawidłową wartość")
            powtorzyc = click.prompt("Tak/Nie", type=str)

        if powtorzyc == 'tak':
            gsd = click.prompt("Podaj GSD [m]", type=float)
            Lx, Ly, Bx, By, _, _, _, Ny, Nx = calc_and_print_params(lX, lY, p, q, DX, DY, gsd, cycle, s)
    click.echo("Rysowanie projektu nalotu")
    fig, ax = plt.subplots()
    color = 'blue'
    # remove 1 cycle from the start
    x_start = Xmin - (Lx - Bx)
    for i in range(Ny):
        for j in range(Nx):
            x = x_start + j * (Lx - Bx)
            y = Ymin + i * (Ly - By)
            # rect = matplotlib.patches.Rectangle((x_start + j * (Lx - Bx), Ymin + i * (Ly - By)), Lx, Ly, edgecolor=color, facecolor='none')
            rect = matplotlib.patches.Rectangle((x, y), Lx, Ly, edgecolor=color, facecolor='none')
            ax.add_patch(rect)
            # add a red point in the middle of the rectangle
            ax.plot(x + Lx / 2, y + Ly / 2, 'ro')
    # set automatic axis scaling
    ax.autoscale()
    plt.show()


if __name__ == '__main__':
    main()
