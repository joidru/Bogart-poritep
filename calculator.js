const calculator = document.querySelector('#gasCalculator');

const field = (form, name) => form.querySelector(`[name="${name}"]`);
const number = (form, name) => Math.max(0, Number(field(form, name).value) || 0);
const decimal = value => new Intl.NumberFormat('ru-RU', {maximumFractionDigits: 1}).format(value);
const integer = value => new Intl.NumberFormat('ru-RU').format(Math.ceil(value));

function calculateGasBlocks() {
  const length = number(calculator, 'length');
  const width = number(calculator, 'width');
  const height = number(calculator, 'height');
  const floors = number(calculator, 'floors');
  const outerThickness = number(calculator, 'outerThickness') / 1000;
  const openings = number(calculator, 'openings');
  const bearingLength = number(calculator, 'bearingLength');
  const bearingThickness = number(calculator, 'bearingThickness') / 1000;
  const partitionLength = number(calculator, 'partitionLength');
  const partitionThickness = number(calculator, 'partitionThickness') / 1000;
  const reserve = number(calculator, 'reserve') / 100;
  const blockHeight = number(calculator, 'blockHeight') / 1000;
  const density = field(calculator, 'density').value;

  const outerGross = 2 * (length + width) * height * floors * outerThickness;
  const outer = Math.max(0, outerGross - openings * outerThickness);
  const bearing = bearingLength * height * floors * bearingThickness;
  const partitions = partitionLength * height * floors * partitionThickness;
  const inner = bearing + partitions;
  const total = (outer + inner) * (1 + reserve);
  const blockVolume = .625 * blockHeight * outerThickness;
  const blocks = blockVolume ? total / blockVolume : 0;
  const pallets = total / 1.875;
  const glue = total / 1.5;
  const pricePerM3 = density === 'D600' ? 7150 : density === 'D500' ? 7000 : 7000;

  document.querySelector('#resultVolume').textContent = decimal(total);
  document.querySelector('#resultOuter').textContent = `${decimal(outer)} м³`;
  document.querySelector('#resultInner').textContent = `${decimal(inner)} м³`;
  document.querySelector('#resultBlocks').textContent = `${integer(blocks)} шт.`;
  document.querySelector('#resultPallets').textContent = `${integer(pallets)} шт.`;
  document.querySelector('#resultGlue').textContent = `${integer(glue)} уп.`;
  document.querySelector('#resultPrice').textContent = `${new Intl.NumberFormat('ru-RU').format(Math.ceil(total * pricePerM3 / 100) * 100)} ₽`;
}

calculator.addEventListener('submit', event => {
  event.preventDefault();
  calculateGasBlocks();
  document.querySelector('#calculatorResult').scrollIntoView({behavior: 'smooth', block: 'nearest'});
});

calculator.addEventListener('input', calculateGasBlocks);
calculator.addEventListener('change', calculateGasBlocks);
calculateGasBlocks();
