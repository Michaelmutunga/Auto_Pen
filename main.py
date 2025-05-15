from scanners.port_scanner import scan_target

if __name__ == "__main__":
    target = input("Enter target IP or domain: ")
    scan_target(target)

